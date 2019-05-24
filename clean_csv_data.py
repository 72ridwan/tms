import os

header = ["object_probs", "left", "top", "right", "bottom"]
path = "frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda utara 1200_x264.mp4"
csv_files = os.listdir(path)

for filename in csv_files:
    fname, fext = os.path.splitext(filename)
    if fext.lower() != '.csv':
        continue
    
    print("Processing", filename + '...')
    output = []
    output += [header]
    
    filepath = path + '/' + filename
    
    with open(filepath, 'r') as infile:
        lines = infile.read().splitlines()
        content = lines[1:]
        
        for i in range(len(content)):
            line = content[i]
            tokens = line.split(',')
            tokens = [i.strip() for i in tokens]
            final_token = []
            # Standard: a line has 6 tokens
            if len(tokens) == 6:
                final_token = [tokens[0] + ' ' + tokens[1]] + tokens[2:]
            else:
                assumptions = (len(tokens) - 4) // 2
                final_token = []
                objects = []
                for j in range(assumptions):
                    objects.append(tokens[j * 2] + ' ' + tokens[j * 2 + 1])
                final_token.append(' '.join(objects))
                final_token += tokens[assumptions * 2:]
            output.append(final_token)
            
    with open(filepath, 'w') as outfile:
        outfile.write('\n'.join([','.join([j for j in lines]) for lines in output]))