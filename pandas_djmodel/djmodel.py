#!/usr/bin/env python
# coding=utf-8
import collections
import math
import re
import unicodedata


def translit(s):
    return unicodedata.normalize('NFKC', unicode(s))


def camel_case(s):
    s = s if not s.isupper() else s.title()
    s = re.sub(r"^[\-_\.]", '', s)
    return s[0].lower() + re.sub(r"[\-_\.\s]([a-z])", lambda m: m.group(1).upper(), s[1:]).replace(' ', '')


def snake_case(s):
    s = s if not s.isupper() else s.lower()
    s = re.sub(r"[\-\.\s]", '_', s)
    return s[0] + re.sub(r"[A-Z]", lambda m: '_' + m.group(0), s[1:]).lower()


def nans_count(col_series):
    return col_series.isnull().sum()


def max_col_str_length(col_series, **kwargs):
    max_length = col_series.astype('str').str.len().max()
    length = int(math.ceil(max_length*1.3/10.0))*10

    return dict(attr='max_length', val=length, hint='max length was %d' % max_length)


def numeric_stats(col_series, **kwargs):
    hint = 'min: %s, max: %s, mean: %s' % (col_series.min(), col_series.max(), col_series.mean())
    return dict(hint=hint)


def can_be_null(col_series, **kwargs):
    return dict(attr='null', val=True) if nans_count(col_series) else {}


def has_nans(col_series, **kwargs):
    count = nans_count(col_series)
    if not count:
        return {}

    return dict(hint='(!) contains %d Nones (%.2f%%)' % (count, float(count)/len(col_series)*100))


def precise_int_field(col_series, **kwargs):
    override = 'IntegerField'
    cmin, cmax = col_series.min(), col_series.max()

    if cmin >= 0 and cmax <= 32768:
        override = 'PositiveSmallIntegerField'
    elif cmin >= -32768 and cmax <= 32768:
        override = 'SmallIntegerField'
    elif cmin > -2147483647 and cmax > 2147483647:
        override = 'BigIntegerField'

    return dict(field_override=override)


def mk_model(df, col_casing='snake'):
    UNSUPPORTED_DTYPE = ('CharField', [lambda x: dict(hint='Unsupported dtype %s' % x.dtype)])
    TYPES_MAP = {  # pandas dtype: (models.Field, callbacks)
        'O': ('CharField', [max_col_str_length, has_nans]),
        'i': ('IntegerField', [can_be_null, has_nans, numeric_stats, precise_int_field]),
        'f': ('FloatField', [can_be_null, has_nans, numeric_stats]),
        'b': ('BooleanField', []),
        'M': ('DateTimeField', [can_be_null]),
        'm': ('DurationField', [can_be_null]),
    }

    case_func = dict(snake=snake_case, camel=camel_case).get(col_casing, None)
    cols = collections.OrderedDict([(col, df[col].dtype.kind) for col in df.columns])

    model_cols = []
    for col, col_dtype in cols.items():
        dj_field, callbacks = TYPES_MAP.get(col_dtype, UNSUPPORTED_DTYPE)
        cb_res = [one(df[col]) for one in callbacks]

        field_overrides = list(filter(None, [one.get('field_override', None) for one in cb_res]))
        dj_field = dj_field if not field_overrides else field_overrides[-1]

        new_col_name = (case_func(col) if case_func else col).strip()
        model_cols.append((new_col_name, (dj_field, cb_res)))

    return collections.OrderedDict(model_cols)


def repr_model(fields, indent=4, hints=True, model_name='DFModel'):
    out = 'class %s(models.Model):\n' % model_name

    for fname, fopts in fields.items():
        field, opts = fopts

        hints_vals, field_opts = [], []
        for one in opts:
            if one.get('attr', None):
                field_opts.append((one['attr'], one['val']))
            if one.get('hint', None):
                hints_vals.append(one['hint'])

        out += '%(indent)s%(fname)s = %(field)s(%(attrs)s)%(hints)s\n' % dict(
            indent=' '*indent,
            fname=fname,
            field='models.%s' % field,
            attrs=', '.join(
                ['%s=%s' % o for o in field_opts]),
            hints=' # '+'; '.join(hints_vals) if hints else '',

            )

    return out


def get_model_repr(df, col_casing='snake', indent=4, hints=True, model_name='DFModel'):
    return repr_model(mk_model(df, col_casing=col_casing), indent=indent, hints=hints, model_name=model_name)
