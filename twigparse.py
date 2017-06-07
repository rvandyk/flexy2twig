import re
from collections import deque

def difflog(fin,fout):
    n = 0
    with open(fin, 'r') as file1:
        with open(fout, 'r') as file2:
                with open('log.txt', 'w') as file_out:
                    art = '''
  _____ ____ _____   ____ ___ _____ _____   _     ___   ____
 |  ___|___ \_   _| |  _ \_ _|  ___|  ___| | |   / _ \ / ___|
 | |_    __) || |   | | | | || |_  | |_    | |  | | | | |  _
 |  _|  / __/ | |   | |_| | ||  _| |  _|   | |__| |_| | |_| |
 |_|   |_____||_|   |____/___|_|   |_|     |_____\___/ \____|

                   '''
                    file_out.write(art + "\n\n\n\n")
                    while(True):
                        n += 1
                        l1 = file1.readline()
                        l2 = file2.readline()
                        if(not l1):
                            file_out.write("\n\n\n#######\nLINE " + str(n) + "\n#######\n\n\n")
                            file_out.write("FLEXY : NOTHING" + "\n====TWIG====> " + l2 + "\n\n--------------------------------------------------------------")
                        if(not l2):
                            file_out.write("\n\n\n#######\nLINE " + str(n) + "\n#######\n\n\n")
                            file_out.write("FLEXY : " + l1 +  " \n====TWIG====> " + "NOTHING" + "\n\n--------------------------------------------------------------")
                        if((not l1) and (not l2)):
                            break
                        if(l1 != l2):
                            file_out.write("\n\n\n#######\nLINE " + str(n) + "\n#######\n\n\n")
                            file_out.write("FLEXY : " + l1 +  " \n====TWIG====> " + l2 + "\n\n--------------------------------------------------------------")


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
            for key in vardict:
                line = re.sub(r"(" + re.escape(key) + r")", "{{ " + vardict[key] + " }}", line)



        o.write(line)
