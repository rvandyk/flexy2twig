#coding: iso8859-15
import re
from collections import deque
from collections import defaultdict

currentbox = deque()
foreachbox = defaultdict(deque)
vardict = dict()
added_line = False


def jump_lines(code):
    """
    Jumps line if there are 2 {} blocks or 2 <> blocks on the same line to simplify processing
    """
    res = ""
    for line in code.splitlines():

        if(re.search(r"({(.*)}(.*){(.*)})+", line)):
            line = re.sub("{", "\n{", line)
        if(re.search(r"(<(.*)>(.*)<(.*)>)+", line)):
            line = re.sub("<", "\n<", line)
        res += line + "\n"
    return res


def detect_script(line):
    """
    Detects script blocks
    """
    script = False
    if(re.search(r"<script type=\"text/javascript\">", line)):
        script = True
    if(re.search(r"</script>", line)):
        script = False
    return script


def sub_filters(line):
    """
    Translates var filters
    """
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
    return line


def script_handler(line):
    """
    Script blocks processing
    """
    for key in vardict:
        line = re.sub(r"(" + re.escape(key) + r")",
                      "{{ " + vardict[key] + " }}", line)
    return line


def nscript_handler(line):
    """
    Not-script blocks handler
    """
    global currentbox
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
    return line


def var_declarations(line):
    """
    Handles js var declarations (outside script blocks)
    """
    global vardict
    m = re.search(
        r"<flexy:toJavascript (?P<var_name>.+)={(?P<var_value>.+)}>", line)
    line = re.sub(r"</flexy:toJavascript>", '', line)
    if(m):
        line = ""
        m = m.groupdict()
        vardict.update({m['var_name']: m['var_value']})
    return line


def cond_loops_handler(line):
    """
    Handles conditions and loops
    """
    global currentbox
    global foreachbox
    global added_line
    res = ""
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
    return line


def parse(code):

    script = False
    ret = ""
    content = ""
    global added_line

    content = jump_lines(code)

    for line in content.splitlines():

        added_line = False  # line added by in-tag if/for ?

        script = detect_script(line)

        line = var_declarations(line)

        line = cond_loops_handler(line)

        line = sub_filters(line)

        if(not script):
            line = nscript_handler(line)
        else:
            line = script_handler(line)

        ret += line + "\n"

    return ret
