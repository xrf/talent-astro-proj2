# Originally by Kevin Siegl.
import struct
import numpy as np

def read_raw(f, fmt):
    '''Reads a raw binary structure from a file-like object with the given
    record format.  (See Python docs for `struct` for more info on the
    format.)'''
    fmt = "".join(fmt)
    return struct.unpack(fmt, f.read(struct.calcsize(fmt)))

def read_fortran(f, fmt):
    '''Reads a Fortran record from a file-like object with the given record
    format.  (See Python docs for `struct` for more info on the format.)'''
    # use little-endian (why?) and add the record lengths that occur at the
    # beginning and the end of the record; the record lengths are not returned
    fmt = "".join(fmt)
    return read_raw(f, "<i" + fmt + "i")[1:-1]

def read_tso(filename):
    '''Reads the `tso` output from XNet.  The naming convention follows that
    of the Fortran code.  Returns a `dict` all the data and parameters.'''
    ret = {}
    with open(filename, "rb") as f:

        descript1, descript2, descript3, ret["data_desc"] = \
            tuple(x.strip() for x in read_fortran(f, ["80s"] * 4))
        ret["descript"] = [descript1, descript2, descript3]

        rec_def = [
            ("i", "kstmx"),
            ("i", "kitmx"),
            ("i", "iweak"),
            ("i", "iscrn"),
            ("i", "iconvc"),
            ("d", "changemx"),
            ("d", "tolm"),
            ("d", "tolc"),
            ("d", "yacc"),
            ("d", "ymin"),
            ("d", "tdel_mm"),
        ]
        rec_types  = (x for x, _ in rec_def)
        rec_names  = (x for _, x in rec_def)
        rec_values = read_fortran(f, rec_types)
        ret.update(dict(zip(rec_names, rec_values)))

        ret["inab_file"], ret["abund_desc"] = \
            tuple(x.strip() for x in read_fortran(f, ["80s"] * 2))

        ret["thermo_file"], ret["thermo_desc"] = \
            tuple(x.strip() for x in read_fortran(f, ["80s"] * 2))

        _         = read_raw(f, "<i")
        ny,       = read_raw(f, "<i")
        ret["zz"] = np.array(read_raw(f, "<" + "d" * ny))
        ret["aa"] = np.array(read_raw(f, "<" + "d" * ny))
        _         = read_raw(f, "<i")
        ret["ny"] = ny

        _               = read_raw(f, "<i")
        mflx,           = read_raw(f, "<i")
        ret["ifl_orig"] = np.array(read_raw(f, "<" + "i" * mflx))
        ret["ifl_term"] = np.array(read_raw(f, "<" + "i" * mflx))
        _               = read_raw(f, "<i")
        ret["mflx"]     = mflx

        rec_def_s = [
            ("i", "kstep"),
            ("d", "t"),
            ("d", "t9t"),
            ("d", "rhot"),
            ("d", "tdel"),
            ("d", "edot"),
        ]
        rec_def = rec_def_s + [
            ("d" * ny, "y"),
            ("d" * mflx, "flx"),
        ]
        rec_types   = tuple(x for x, _ in rec_def)
        rec_names_s = tuple(x for _, x in rec_def_s)
        for name in rec_names_s:
            ret[name] = []
        y   = []
        flx = []
        # read until end
        while True:
            try:
                rec_values = read_fortran(f, rec_types)
            except:
                break
            for name, value in zip(rec_names_s, rec_values):
                ret[name].append(value)
            y_start = len(rec_names_s)
            y_end   = y_start + ny
            y.append(rec_values[y_start:y_end])
            flx_start = y_end
            flx_end   = flx_start + mflx
            flx.append(rec_values[flx_start:flx_end])

    # convert into numpy arrays
    for name in rec_names_s:
        ret[name] = np.array(ret[name])
    ret["y"]   = np.transpose(np.array(y))
    ret["flx"] = np.transpose(np.array(flx))

    return ret
