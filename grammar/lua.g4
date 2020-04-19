grammar lua;

root: block EOF?;

block : (statements+=statement (';')?)* (return_statement (';')?)?;
return_statement : 'return' (rvalue_handle)? | 'break';

statement :  lvalue_handle '=' rvalue_handle #lb_assignment_statement |
	function_call_statement #lb_call_statement |
	'do' block 'end' #lb_do_statement |
	'while' expression 'do' block 'end' #lb_while_statement |
	'repeat' block 'until' expression #lb_repeat_until_statement |
	'if' expression 'then' block ('elseif' expression 'then' block)* ('else' block)? 'end' #lb_conditional_statement |
	'for' NAME '=' expression ',' expression (',' expression)? 'do' block 'end' #lb_for_statement |
	'for' lvalue_identifiers_list 'in' rvalue_handle 'do' block 'end' #lb_foreach_statement |
	'function' top_level_name=NAME ('.' class_level_name=NAME)* (':' class_level_name=NAME)? function_body #lb_function_declaration_statement |
	'local' 'function' NAME function_body #lb_local_function_declaration_statement |
	'local' lvalue_identifiers_list ('=' rvalue_handle)? #lb_local_lvalue_declaration_statement ;

lvalue_handle : expressions+=expression_assignable (',' expressions+=expression_assignable)*;
lvalue_identifiers_list : NAME (',' NAME)*;
rvalue_handle : (expressions+=expression ',')* expressions+=expression;

expression:
    'nil' #lb_nil_literal_expression
    | 'false' #lb_false_literal_expression
    | 'true'  #lb_true_literal_expression
    | number #lb_number_literal_expression
    | string #lb_string_literal_expression
    | '...' #lb_ellipsis_literal_expression
    | function #lb_function_declaration_expression
    | table_declaration #lb_table_declaration_expression
    | '(' expression ')' #lb_brackets_expression
    | operation=('not' | '#' | '-' | '~') right=expression                          #lb_unary_expression
    | left=expression operation=( '*' | '/' | '%' | '//') right=expression          #lb_binary_term_expression
    | left=expression operation=( '+' | '-' ) right=expression                      #lb_binary_expr_expression
    | <assoc=right> left=expression operation='..' right=expression                 #lb_concat_expression
    | left=expression operation=('<' | '>' | '<=' | '>=' | '~=' | '==') right=expression #lb_logic_equal_expression
    | left=expression operation='and' right=expression                                   #lb_logic_and_expression
    | left=expression operation='or' right=expression                             #lb_logic_or_expression
    | right=expression operation=('&' | '|' | '~' | '<<' | '>>') right=expression #lb_bit_expression
    | expression_value #lb_value_expression
    | expression_access_by_index #lb_access_by_index_expression
    | expression_call #lb_call
;

expression_value: NAME (':' NAME)?;
expression_access_by_index: expression_accessible_by_index '[' expression ']';
expression_call: expression_callable '(' (rvalue_handle)? ')';

expression_accessible_by_index: expression_value | string;
expression_callable: expression_value | string;
expression_assignable: expression_value;

function_call_statement: NAME (':' NAME)? '(' (rvalue_handle)? ')';

function : 'function' function_body;
function_body : '(' (function_parameters_list)? ')' block 'end';
function_parameters_list : lvalue_identifiers_list (',' ellipsis='...')? | ellispis='...';

table_declaration : '{' (table_fields)? '}';
table_fields : table_field_declaration (fields_separator table_field_declaration)* (fields_separator)?;
table_field_declaration : '[' expression ']' '=' expression | NAME '=' expression | expression;

fields_separator : ',' | ';';

number : INT | FLOAT | EXP | HEX;
string	: NORMALSTRING | CHARSTRING | LONGSTRING;

// TOKENS
NAME: [a-zA-Z_][a-zA-Z_0-9]*;

INT	: ('0'..'9')+;
FLOAT 	:INT '.' INT;
EXP: (INT| FLOAT) ('E'|'e') ('-')? INT;
HEX: '0x' ('0'..'9'| 'a'..'f')+;

NORMALSTRING:  '"' ( EscapeSequence | ~('\\'|'"') )* '"';
CHARSTRING:	'\'' ( EscapeSequence | ~('\''|'\\') )* '\'';
LONGSTRING:	'['('=')*'[' ( EscapeSequence | ~('\\'|']') )* ']'('=')*']';

fragment
EscapeSequence: '\\' ('b'|'t'|'n'|'f'|'r'|'\\"'|'\''|'\\') |   UnicodeEscape |   OctalEscape;

fragment
OctalEscape: '\\' ('0'..'3') ('0'..'7') ('0'..'7') | '\\' ('0'..'7') ('0'..'7') | '\\' ('0'..'7');

fragment
UnicodeEscape: '\\' 'u' HexDigit HexDigit HexDigit HexDigit;

fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;

COMMENT: '--[[' ()* ']]' -> skip;
LINE_COMMENT: '--' ~('\n'|'\r')* '\r'? '\n' -> skip;
WS: [ \t\u000C\r\n]+ -> skip;
