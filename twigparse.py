import re
from collections import deque

def parse(fin,fout):
    f = open(fin, 'r')
    o = open(fout, 'w')

    currentbox = deque()
    vardict = dict()
    script = False

    for line in f:
        if(re.search(r"<script type=\"text/javascript\">",line)):
            script = True
        if(re.search(r"</script>",line)):
            script = False
        m = re.search(r"<flexy:toJavascript (?P<var_name>.+)={(?P<var_value>.+)}></flexy:toJavascript>",line)
        if(m):
            line = ""
            m.groupdict()
            print(m['var_name'] + '=' + m['var_value'])
            vardict.update({m['var_name'] :  m['var_value']})

        if(re.search(r"({if)", line)):
            currentbox.append("if")
        if(re.search(r"({foreach)", line)):
            ex = re.split('foreach|\t|,|:|{|}|\n',line)
            ex = [x for x in ex if x != '']
            res = '{ for ' + ex[1]
            for i in range (2,len(ex)):
                res += ','+ ex[i]
            res += ' in ' + ex[0] + " }"
            line = re.sub(r"({foreach:)(.*)[}]+", res, line)
            currentbox.append("for")

        if(not script):
            line = re.sub(r"[:]", " ", line)
            line = re.sub(r"[{]", "{% ", line)
            line = re.sub(r"[}]", " %}", line)
            if(re.search(r"({% end)",line)):
                line = re.sub(r"({% end)", "{% end" + currentbox.pop(), line)
            line = re.sub(r"<flexy include src=", "{% include ", line)
            line = re.sub(r"></flexy include>", " %}", line)
            line = re.sub(r"\#", "\"", line)
        if(script):
            print('in a script....')
            for key in vardict:
                print("Looking for "+key)
                line = re.sub(r"(" + re.escape(key) + r")", "{{ " + vardict[key] + " }}", line)



        o.write(line)
