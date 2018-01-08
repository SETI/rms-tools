################################################################################
# Usage: python make_vectorize_i.py >vectorize.i
#
# This progrmm generates file vectorize.i by creating a macro that defines the
# inline code for the signature of each SWIG interface to a CSPICE function.
################################################################################

class Arg(object):
    pass

def print_vectorization_macro(fullname):

    ### Interpret the encoded name

    if not fullname.startswith('VECTORIZE_'):
        raise ValueError('Invalid name: ' + fullname)

    argstring = fullname[len('VECTORIZE_'):]

    (inarg_string, outarg_string) = argstring.split('__')

    # Extract a RETURN indicator
    use_return = outarg_string.startswith('RETURN')
    if use_return:
        outarg_string = outarg_string[len('RETURN_')]

    # Replace '2d' with 'd','d', etc.
    arg_keys = []
    for arg_string in (inarg_string, outarg_string):
        parts = arg_string.split('_')

        parsed = []
        for part in parts:
            if part[0] in '23456789':
                count = int(part[0])
                part = part[1:]
                parsed += count * [part]
            else:
                parsed.append(part)

        arg_keys.append(parsed)

    (inarg_keys, outarg_keys) = arg_keys

    ### MACRO HEADER

    # Identify capital letters which will need to be defined in the macro
    out_letters = []
    for key in outarg_keys:
        for c in key[1:]:
            if c in 'IJKLMN':
                out_letters.append(c)

    print
    len_letters = len(out_letters)
    if len_letters == 0:
        print '%%define %s(NAME, FUNC)' % fullname
    else:
        print '%%define %s(NAME, FUNC,' % fullname,
        for k in range(len_letters-1):
            print out_letters[k] + ',',
        print out_letters[-1] + ')'

    print

    ### Interpret the input argument keys

    s_count = 0
    i_count = 0
    de_counts = {
        'd': [0, 0, 0, 0],  # For ConstSpiceDouble
        'e': [0, 0, 0, 0],  # For SpiceDouble
    }
    de_type = {
        'd': 'ConstSpiceDouble *',
        'e': 'SpiceDouble *',
    }

    ijkdict = {}    # Maps lowercase indices (i,j,k) to input argument names

    inargs = []
    sizers = []
    for key in inarg_keys:
        arg = Arg()
        arg.key = key
        arg.char = key[0]
        arg.comma1 = ','    # used after declaration
        arg.comma2 = ','    # used after function call
        arg.is_lower = False

        if key == 's':
            s_count += 1
            arg.name = 'str%d' % s_count
            arg.rank = 0
            arg.declaration = 'ConstSpiceChar *' + arg.name
        elif key == 'i':
            i_count += 1
            arg.name = 'k%d' % i_count
            arg.rank = 0
            arg.declaration = 'SpiceInt ' + arg.name
        elif key[0] in 'de':
            arg.rank = len(key)
            de_counts[key[0]][arg.rank] += 1
            arg.name = 'in%d%d' % (arg.rank, de_counts[key[0]][arg.rank])
            arg.is_lower = key[-1].lower() == key[-1]   # i, j, k, etc.
            arg.dim_names = [arg.name + '_dim1']
            parts = [de_type[key[0]] + arg.name, 'int ' + arg.dim_names[0]]
            for k in range(1,arg.rank):
                dim_name = arg.name + '_dim' + str(k+1)
                letter = key[k]
                if arg.is_lower:
                    ijkdict[letter] = dim_name
                arg.dim_names.append(dim_name)
                parts.append('int ' + dim_name)
            arg.declaration = ', '.join(parts)
            sizers.append(arg.dim_names[0])
        else:
            raise ValueError('Unrecognized input arg in ' + fullname)

        inargs.append(arg)

    # Define how to include each input item in the call
    for arg in inargs:
        if arg.rank == 0:
            arg.call = arg.name
            continue

        if len(sizers) == 1:
            indexer = 'i'
        else:
            indexer = 'i %% %s' % arg.dim_names[0]

        parts = [arg.name]
        if arg.rank == 1:
            parts += ['[', indexer, ']']
        else:
            parts += [' + (', indexer, ')']

        for dim_name in arg.dim_names[1:]:
            parts += [' * ', dim_name]

        if arg.is_lower:
            for dim_name in arg.dim_names[1:]:
                parts += [', ', dim_name]

        arg.call = ''.join(parts)

    ### Interpret the output argument keys

    b_count = 0
    i_count = 0
    d_counts = [0, 0, 0, 0]

    outargs = []
    for key in outarg_keys:
        arg = Arg()
        arg.key = key
        arg.char = key[0]
        arg.comma1 = ','    # used after declaration
        arg.comma2 = ','    # used after function call
        arg.is_lower = False

        if key == 'i':
            i_count += 1
            arg.name = 'int%d' % i_count
            arg.rank = 1
            arg.dim_names = [arg.name + '_dim1']
            arg.dim_values = ['']
            arg.declaration = 'SpiceInt **%s, int *%s' % (arg.name,
                                                          arg.dim_names[0])
            arg.malloc = ('SpiceInt *%s_buffer = ' % arg.name +
                          'my_int_malloc(size, my_name);')
        elif key == 'b':
            b_count += 1
            arg.name = 'bool%d' % b_count
            arg.rank = 1
            arg.dim_names = [arg.name + '_dim1']
            arg.dim_values = ['']
            arg.declaration = 'SpiceBoolean **%s, int *%s' % (arg.name,
                                                              arg.dim_names[0])
            arg.malloc = ('SpiceBoolean *%s_buffer = ' % arg.name +
                          'my_bool_malloc(size, my_name);')
            arg.dim_names = [arg.name + '_dim1']
            arg.dim_values = ['']
        elif key[0] == 'd':
            arg.rank = len(key)
            d_counts[arg.rank] += 1
            arg.name = 'out%d%d' % (arg.rank, d_counts[arg.rank])
            arg.dim_names = [arg.name + '_dim1']
            arg.dim_values = ['']
            arg.is_lower = key[-1].lower() == key[-1]   # i, j, k, etc.
            parts = ['SpiceDouble **%s' % arg.name,
                     'int *%s' % arg.dim_names[0]]
            for k in range(1,arg.rank):
                dim_name = arg.name + '_dim' + str(k+1)
                letter = key[k]
                if letter == letter.lower():
                    dim_value = ijkdict[letter]
                else:
                    dim_value = letter
                arg.dim_names.append(dim_name)
                arg.dim_values.append(dim_value)
                parts.append('int *%s' % dim_name)
            arg.declaration = ', '.join(parts)

            parts = ['SpiceDouble *%s_buffer = my_malloc(size' % arg.name] + \
                    arg.dim_values[1:]
            arg.malloc = ' * '.join(parts) + ', my_name);'
        else:
            raise ValueError('Unrecognized input arg in ' + fullname)

        outargs.append(arg)

    # Define how to include each input item in the call
    for arg in outargs:
        parts = [arg.name, '_buffer + i']

        for dim_value in arg.dim_values[1:]:
            parts += [' * ', dim_value]

        if arg.is_lower:
            for dim_name in arg.dim_names[1:]:
                parts += [', ', dim_name]

        arg.call = ''.join(parts)

    # No comma after the last declaration
    outargs[-1].comma1 = ''

    # No comma after the last argument in the function call
    if use_return:
        outargs[0].comma2 = ''
        inargs[-1].comma2 = ''
    else:
        outargs[-1].comma2 = ''

    ### FUNCTION DECLARATION

    print '%apply (void RETURN_VOID) {void NAME ## _vector};'
    print

    print '%inline %{'
    print '    void NAME ## _vector('

    for arg in inargs + outargs:
        print 8 * ' ' + arg.declaration + arg.comma1

    print '    ) {'
    print
    print 8*' ' + 'char *my_name = "NAME" "_vector";'
    print

    # Initialize return variables
    for k in range(len(outargs)):
        arg = outargs[k]
        print 8*' ' + '*%s = NULL;' % arg.name
        print 8*' ' + '*%s = 0;' % arg.dim_names[0]
        for (name, value) in zip(arg.dim_names, arg.dim_values)[1:]:
            print 8*' ' + '*%s = %s;' % (name, value)

        print

    # Get maximum leading dimensions
    print 8*' ' + 'int maxdim = %s;' % sizers[0]
    for sizer in sizers[1:]:
        print 8*' ' + 'if (maxdim < %s) maxdim = %s;' % (sizer, sizer)
    print
    print 8*' ' + 'int size = (maxdim == 0 ? 1 : maxdim);'
    for sizer in sizers:
        print 8*' ' + '%s = (%s == 0 ? 1 : %s);' % (sizer, sizer, sizer)
    print

    # Allocate output arrays
    for k in range(len(outargs)):
        arg = outargs[k]
        print 8*' ' + arg.malloc

        if k == 0:
          print 8*' ' + 'if (!%s_buffer) return;' % arg.name

        else:
          print 8*' ' + 'if (!%s_buffer) {' % arg.name
          for kk in range(k):
            print 12*' ' + 'free(%s_buffer);' % outargs[kk].name
          print   12*' ' + 'return;'
          print 8*' ' + '}'

        print

    # Loop through values
    print 8*' ' + 'for (int i = 0; i < size; i++) {'

    # Execute function inside loop
    if use_return:
        print 12*' ' + '%s_buffer[i] = FUNC(' % outargs[0].name
    else:
        print 12*' ' + 'FUNC('

    # Insert input arguments into function
    for arg in inargs:
        print 16*' ' + arg.call + arg.comma2

    if not use_return:
        for arg in outargs:
            print 16*' ' + arg.call + arg.comma2

    print 12*' ' + ');'

    # End of loop
    print '        }'
    print

    # Return pointers to the allocated buffers
    for k in range(len(outargs)):
        arg = outargs[k]
        print 8*' ' + '*%s = %s_buffer;' % (arg.name, arg.name)
        print 8*' ' + '*%s = maxdim;' % arg.dim_names[0]
        for (name, value) in zip(arg.dim_names, arg.dim_values)[1:]:
            print 8*' ' + '*%s = %s;' % (name, value)

        if k < len(outargs) - 1:
            print

    print '    }'

    # End of inline

    print '%}'
    print

    # End of macro

    print '%enddef'
    print
    print '/' + 78*'*' + '/'

# Print the header
print '/' + 131 * '*'
print '* cspyce0/vectorize.i'
print '*'
print '* This file is automatically generated by program make_vectorize.py. To regenerate:'
print '*     python make_vectorize.py >vectorize.i'
print '*'
print '* This file begins with an exact copy of file vectorize_header.txt. '  +\
        'This is followed by a sequence of SWIG macro definitions, one'
print '* for each of the names listed in file vectorize_names.txt. Each '     +\
        'macro name defines a sequence of input arguments followed by a'
print '* sequence of output arguments. Program make_vectorize.py interprets ' +\
        'the name of the macro and defines a SWIG inline function that'
print '* handles that sequence of arguments. Inside the file cspyce0.i, each '+\
        'function is vectorized by executing one of these macros, which'
print '* then expands into the needed inline source code.'
print 131 * '*' + '/'
print

# Define the typemaps
f = open('vectorize_header.txt')
for rec in f:
    print rec[:-1]
f.close()

# Print a macro for each name
f = open('vectorize_names.txt')
names = [rec[:-1] for rec in f]
f.close()

for name in names:
    print_vectorization_macro(name)

