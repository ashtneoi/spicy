GRAMMAR = r"""
start = line*
line = ws [NAME ":" ws] [insn ws] [comment ws] "\n"

insn = OPC_FD WSR expr [ws "," ws /[WF]/]
     | OPC_F WSR expr
     | OPC_X
     | OPC_FB WSR expr ws "," ws expr
     | OPC_K WSR expr
     | OPC_PC WSR expr
     | OPC_TR WSR expr
     | OPC_NK WSR expr ws "," ws expr
     | OPC_NM WSR (fsr_pre | fsr_post)
     | OPC_IN WSR expr_closed ws "[" ws "FSR" ("0" | "1") ws "]"
     | ".def" ws NAME ws "," ws expr

OPC_FD = "addwf" | "addwfc" | "andwf" | "asrf" | "lslf" | "lsrf" | "comf"
       | "decf" | "incf" | "iorwf" | "movf" | "rlf" | "rrf" | "subwf"
       | "subwfb" | "swapf" | "xorwf" | "decfsz" | "incfsz"
OPC_F = "clrf" | "movwf"
OPC_X = "clrw" | "brw" | "callw" | "retfie" | "return" | "clrwdt" | "nop"
      | "option" | "reset" | "sleep"
OPC_FB = "bcf" | "bsf" | "btfsc" | "btfss" | "ifc" | "ifs"
OPC_K = "addlw" | "andlw" | "iorlw" | "movlb" | "movlp" | "movlw" | "sublw"
      | "xorlw" | "retlw"
OPC_PC = "bra" | "call" | "goto"
OPC_TR = "tris"
OPC_NK = "addfsr"
OPC_NM = "moviw" | "movwi"
OPC_IN = OPC_NM

ws = [WSR]
WSR = /[ \t]+/

comment = ";" /[^\n]*/

fsr_pre = ("++" | "--") "FSR" ("0" | "1")
fsr_post = "FSR" ("0" | "1") ("++" | "--")

expr_closed = expr5

expr = expr2 (ws ("+" | "-") ws expr2)*
expr2 = expr3 (ws "*" ws expr3)*
expr3 = expr4 (ws ("&" | "|" | "^") ws expr4)*
expr4 = expr5 (ws ("<<" | ">>") ws expr5)*
expr5 = ["-" | "~"] expr6
expr6 = INT | NAME | "(" ws expr ws ")"

INT = /[1-9][0-9_]*/ | /0x[0-9a-fA-F_]+/ | /0n[01_]+/ | /0c[0-7_]+/ | "0"
// yikes
NAME = /[^0-9,.:;()[\]{}'"+\-*\/&|^\\ \t\n][^,.:;()[\]{}'"+\-*\/&|^\\ \t\n]*/
"""
