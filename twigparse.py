#coding: latin-1
import re
from collections import deque
from collections import defaultdict


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


def parse(code):

    currentbox = deque()
    foreachbox = defaultdict(deque)
    vardict = dict()
    script = False
    ret = ""
    med= ""

    for line in code.splitlines():

        #jump lines if necessary
        for i in range (len(line)):
            if((line[i] == "{" and line[i-1] == "}") or (line[i] == "<" and line[i-1] == ">")):
                line = line[:i] + "\n" + line[i:]
        med += line + "\n"



    for line in med.splitlines():

        #script detection
        if(re.search(r"<script type=\"text/javascript\">",line)):
            script = True
        if(re.search(r"</script>",line)):
            script = False

        #var declarations
        m = re.search(r"<flexy:toJavascript (?P<var_name>.+)={(?P<var_value>.+)}></flexy:toJavascript>",line)
        if(m):
            line = ""
            m.groupdict()
            vardict.update({m['var_name'] : m['var_value']})

        #loops/conditions handler

        #if
        if(re.search(r"({if)", line)):
            currentbox.append("if")

        #foreach
        if(re.search(r"({foreach)", line)):
            ex = re.split('foreach|\t|,|:|{|}|\n',line)
            ex = [x for x in ex if x.replace(" ", "") != '']
            res = '{ for ' + ex[1]
            for i in range (2,len(ex)):
                res += ','+ ex[i]
            res += ' in ' + ex[0] + " }"
            line = re.sub(r"({foreach:)(.*)[}]+", res, line)
            currentbox.append("for")

        #if in tags
        t = re.search(r"(<)(?P<tag>[^\s]+)(.*)(flexy:if=\"(?P<args>.+)\")",line)
        if(t):
            line = re.sub(r"(flexy:if=\"(.+)\")", "", line)
            line = "{if " + t['args'] + "}" + "\n" + line
            foreachbox[t['tag']].append('if')

        #foreach in tags
        s = re.search(r"(<)(?P<tag>[^\s]+)(.*)(flexy:foreach=\"(?P<args>.+)\")",line)
        if(s):
            line = re.sub(r"(flexy:foreach=\"(.+)\")", "", line)
            ex = re.split(',', s['args'])
            res = '{ for ' + ex[1]
            for i in range (2,len(ex)):
                res += ','+ ex[i]
            res += ' in ' + ex[0] + " }"
            line = res + '\n' + line
            foreachbox[s['tag']].append('for')





        #close tag
        s = re.search(r"(<(?P<tag>.+)>)", line)
        s = s.groupdict()
        print(s)
        if(s):
            if('tag' in s):
                if((s['tag'] in foreachbox)):
                    foreachbox[s['tag']].append('')


        s = re.search(r"(</(?P<tag>.+)>)", line)
        if(s and (foreachbox[s['tag']])):
            d = foreachbox[s['tag']].pop()
            if(d != ''):
                line = line + "\n" + "{ end" + d + " }"



        #filters
        line = re.sub(r"(:h)", "|raw", line)
        line = re.sub(r"(:u)", "|urlencode", line)
        line = re.sub(r"(:n)", "|number_format", line)
        line = re.sub(r"(:b)", "|nl2br", line)



        #not script handler
        if(not script):
            line = re.sub(r"[:]", " ", line)
            line = re.sub(r"[{]", "{% ", line)
            line = re.sub(r"[}]", " %}", line)
            if(re.search(r"({% end)",line)):
                line = re.sub(r"({% end)", "{% end" + currentbox.pop(), line)
            line = re.sub(r"<flexy include src=", "{% include ", line)
            line = re.sub(r"></flexy include>", " %}", line)
            line = re.sub(r"\#", "\"", line)





        #script handler
        if(script):
            for key in vardict:
                line = re.sub(r"(" + re.escape(key) + r")", "{{ " + vardict[key] + " }}", line)




        ret += line + "\n"
        

    return ret
