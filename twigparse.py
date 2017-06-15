#coding: iso8859-15
import re
from collections import deque
from collections import defaultdict

def parse(code):

    currentbox = deque()
    foreachbox = defaultdict(deque)
    vardict = dict()
    script = False
    ret = ""
    med = ""

    for line in code.splitlines():

        # jump lines if necessary
        # for i in range (len(line)):
            # if((line[i] == "{" and line[i-1] == "}") or (line[i] == "<" and line[i-1] == ">")):
            #line = line[:i] + "\n" + line[i:]
        if(re.search(r"({(.*)}(.*){(.*)})+", line)):
            line = re.sub("{", "\n{", line)
        if(re.search(r"(<(.*)>(.*)<(.*)>)+", line)):
            line = re.sub("<", "\n<", line)
        med += line + "\n"

    for line in med.splitlines():
        added_line = False  # line added by in-tag if/for ?

        # script detection
        if(re.search(r"<script type=\"text/javascript\">", line)):
            script = True
        if(re.search(r"</script>", line)):
            script = False

        # var declarations
        m = re.search(
            r"<flexy:toJavascript (?P<var_name>.+)={(?P<var_value>.+)}>", line)
        line = re.sub(r"</flexy:toJavascript>", '', line)
        if(m):
            line = ""
            m = m.groupdict()
            vardict.update({m['var_name']: m['var_value']})

        # loops/conditions handler

        # if
        if(re.search(r"({if)", line)):
            line = re.sub(r"(!)", " not ", line)
            currentbox.append("if")

        # foreach
        if(re.search(r"({foreach)", line)):
            ex = re.split('foreach|\t|,|:|{|}|\n', line)
            ex = [x for x in ex if x.replace(" ", "") != '']
            res = '{ for ' + ex[1]
            for i in range(2, len(ex)):
                res += ',' + ex[i]
            res += ' in ' + ex[0] + " }"
            line = re.sub(r"({foreach:)(.*)[}]+", res, line)
            currentbox.append("for")

        # if in tags
        t = re.search(
            r"(<)(?P<tag>[^\s]+)(.*)(flexy:if=\"(?P<args>[^\"]+)\")(.*)", line)
        if(t):
            t = t.groupdict()
            line = re.sub(r"(flexy:if=\"([^\"]+)\")", "", line)
            t['args'] = re.sub(r"!", "not ", t['args'])
            if(t['tag'] == "meta"):
                line = "{if " + t['args'] + "}" + "\n" + line + "\n{endif}"
            else:
                line = "{if " + t['args'] + "}" + "\n" + line
                foreachbox[t['tag']].append('if')
                added_line = True

        #foreach in tags
        s = re.search(
            r"(<)(?P<tag>[^\s]+)(.*)(flexy:foreach=\"(?P<args>[^\"]+)\")(.*)", line)
        if(s):
            s = s.groupdict()
            line = re.sub(r"(flexy:foreach=\"([^\"]+)\")", '', line)
            ex = re.split(',', s['args'])
            res = '{ for ' + ex[1]
            for i in range(2, len(ex)):
                res += ',' + ex[i]
            res += ' in ' + ex[0] + " }"
            if(s['tag'] == "meta"):
                line = res + '\n' + line + "\n{endfor}"
            else:
                line = res + '\n' + line
                foreachbox[s['tag']].append('for')
                added_line = True

        # close tag
        s = re.search(r"(<(?P<tag>.+)>)", line)
        if(s):
            s = s.groupdict()
            if('tag' in s):
                if((s['tag'] in foreachbox)):
                    foreachbox[s['tag']].append('')

        s = re.search(r"(</(?P<tag>.+)>)", line)
        if(s):
            s = s.groupdict()
            if(foreachbox[s['tag']]):
                d = foreachbox[s['tag']].pop()
                if(d != ''):
                    line = line + "\n" + "{ end" + d + " }"

        # filters

        line = re.sub(r"(:h)", "|raw", line)
        line = re.sub(r"(:uppercase)", "|bao_uppercase", line)
        line = re.sub(r"(:ucfirst)", "|bao_ucfirst", line)
        line = re.sub(r"(:ucwords)", "|bao_ucwords", line)
        line = re.sub(r"(:u)", "|urlencode", line)
        line = re.sub(r"(:n)", "|number_format", line)
        line = re.sub(r"(:b)", "|nl2br", line)
        line = re.sub(r"(:float)", "|bao_float", line)
        line = re.sub(r"(:int)", "|bao_int", line)
        line = re.sub(r"(:date)", "|bao_date", line)
        line = re.sub(r"(:time)", "|bao_time", line)
        line = re.sub(r"(:lowercase)", "|bao_lowercase", line)
        line = re.sub(r"(:trim)", "|bao_trim", line)
        line = re.sub(r"(:text)", "|bao_text", line)
        line = re.sub(r"(:length)", "|bao_length", line)
        line = re.sub(r"(:phone)", "|bao_phone", line)
        line = re.sub(r"(:price)", "|bao_price", line)
        line = re.sub(r"(:rate)", "|bao_rate", line)
        line = re.sub(r"(:hidden)", "|bao_hidden", line)
        line = re.sub(r"(:visible)", "|bao_visible", line)

        # not script handler
        if(not script):
            if(re.search(r"[:]", line)):
                if(not(re.search(r"\"(.*)[:](.*)\"", line))):
                    line = re.sub(r"[:]", " ", line)
            if(re.search(r"{", line)):
                if(added_line):
                    ls = line.splitlines()
                    ls[0] = re.sub(r"[{]", "{% ", ls[0])
                    ls[0] = re.sub(r"[}]", " %}",  ls[0])
                    ls[1] = re.sub(r"[{]", "{{ ",  ls[1])
                    ls[1] = re.sub(r"[}]", " }}", ls[1])
                    line = ls[0] + "\n" + ls[1]
                elif((re.search(r"for |if |end |else ", line))):
                    line = re.sub(r"[{]", "{% ", line)
                    line = re.sub(r"[}]", " %}", line)
                else:
                    line = re.sub(r"[{]", "{{ ", line)
                    line = re.sub(r"[}]", " }}", line)

            if(re.search(r"({% end  %})", line)):
                line = re.sub(r"({% end)", "{% end" + currentbox.pop(), line)
            m = re.search(r"<flexy include src=(?P<src>.+)>", line)
            if(m):
                m = m.groupdict()
                line = "{{ include (" + m['src'] + ") }}"
            line = re.sub("</flexy include>", "", line)
            if(re.search(r"[#]", line)):
                if(not(re.search(r"\"(.*)[#](.*)\"", line))):
                    line = re.sub(r"\#", "\"", line)

        # script handler
        if(script):
            for key in vardict:
                line = re.sub(r"(" + re.escape(key) + r")",
                              "{{ " + vardict[key] + " }}", line)

        ret += line + "\n"

    return ret
