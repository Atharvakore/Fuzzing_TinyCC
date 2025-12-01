import random
from typing import Generator
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from fuzzingbook.Coverage import Coverage, population_coverage
import project_evaluation  
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
from fuzzingbook.Grammars import opts
from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.MutationFuzzer import FunctionRunner
from fuzzingbook.GreyboxFuzzer import AdvancedMutationFuzzer , Mutator , PowerSchedule   , GreyboxFuzzer 


C_GRAMMAR = {
    # -------------------------------------------------
    # START
    # -------------------------------------------------
    "<start>": [
        ("<pp_section>\n<globals>\n<program>", opts(prob=1.0)),
    ],

    # -------------------------------------------------
    # PREPROCESSOR
    # -------------------------------------------------
    "<pp_section>": [
        ("", opts(prob=0.25)),
        ("<pp_directive>\n<pp_section>", opts(prob=0.75)),
    ],

    "<pp_directive>": [
        ("#define X <int_literal>",                   opts(prob=0.08)),
        ("#define Y (<int_literal> + <int_literal>)", opts(prob=0.08)),
        ("#undef X",                                  opts(prob=0.05)),
        ("#if <int_literal>",                         opts(prob=0.06)),
        ("#ifdef X",                                  opts(prob=0.05)),
        ("#ifndef X",                                 opts(prob=0.05)),
        ("#elif <int_literal>",                       opts(prob=0.05)),
        ("#else",                                     opts(prob=0.04)),
        ("#endif",                                    opts(prob=0.04)),
        ("#line <int_literal>",                       opts(prob=0.20)),
        ("#error \"msg\"",                            opts(prob=0.30)),
    ],

    # -------------------------------------------------
    # GLOBAL DECLARATIONS
    # -------------------------------------------------
    "<globals>": [
        ("", opts(prob=0.20)),
        ("<global_decl>\n<globals>", opts(prob=0.80)),
    ],

    "<global_decl>": [
        ("int g1 = <int_literal>;",                         opts(prob=0.05)),
        ("int g2;",                                         opts(prob=0.05)),
        ("char gbuf[10];",                                  opts(prob=0.05)),
        ("const int C1 = <int_literal>;",                   opts(prob=0.06)),
        ("static int S1 = <int_literal>;",                  opts(prob=0.06)),
        ("extern int ext1;",                                opts(prob=0.06)),
        ("int arr2[5] = {0,1,2,3,4};",                      opts(prob=0.10)),
        ("static int mat[2][2] = {{1,2},{3,4}};",           opts(prob=0.10)),
        ("char hello_str[] = \"Hello\";",                   opts(prob=0.08)),
        ("long big = 0x12345678;",                          opts(prob=0.06)),
        ("struct S { int a; float b; };",                   opts(prob=0.10)),
        ("union U { int x; char c; };",                     opts(prob=0.08)),
        ("typedef struct S SType; SType s_global;",         opts(prob=0.15)),
    ],

    # -------------------------------------------------
    # TYPES
    # -------------------------------------------------
    "<type>": [
        ("int",             opts(prob=0.05)),
        ("char",            opts(prob=0.05)),
        ("long",            opts(prob=0.05)),
        ("short",           opts(prob=0.05)),
        ("unsigned int",    opts(prob=0.05)),
        ("float",           opts(prob=0.05)),
        ("double",          opts(prob=0.05)),
        ("const int",       opts(prob=0.04)),
        ("volatile int",    opts(prob=0.04)),
        ("static int",      opts(prob=0.04)),
        ("extern int",      opts(prob=0.04)),
        ("<pointer_type>",  opts(prob=0.13)),
        ("<struct_type>",   opts(prob=0.20)),
        ("<typedef_type>",  opts(prob=0.16)),
    ],

    "<pointer_type>": [
        ("<type_base>*", opts(prob=1.0)),
    ],

    "<type_base>": [
        ("int",    opts(prob=0.30)),
        ("char",   opts(prob=0.20)),
        ("float",  opts(prob=0.25)),
        ("double", opts(prob=0.25)),
    ],

    "<struct_type>": [
        ("struct <identifier>",                        opts(prob=0.45)),
        ("struct <identifier> { <struct_fields> }",    opts(prob=0.55)),
    ],

    "<struct_fields>": [
        ("<type> <identifier>;",                  opts(prob=0.50)),
        ("<type> <identifier>;\n<struct_fields>", opts(prob=0.50)),
    ],

    "<typedef_type>": [
        ("myint",   opts(prob=0.34)),
        ("mychar",  opts(prob=0.33)),
        ("myfloat", opts(prob=0.33)),
    ],

    # -------------------------------------------------
    # PROGRAM / FUNCTIONS
    # -------------------------------------------------
    "<program>": [
        ("<function_def>",            opts(prob=0.50)),
        ("<function_def>\n<program>", opts(prob=0.50)),
    ],

    "<function_def>": [
        ("<type> <identifier>() { <stmt_list> }",             opts(prob=0.20)),
        ("<type> <identifier>(<param_list>) { <stmt_list> }", opts(prob=0.20)),
        ("int func_fp(int a){ return a+1; }\n"
         "int (*fp)(int);\n"
         "int main(){ fp = func_fp; int r = fp(5); return r; }",
         opts(prob=0.60)),
    ],

    "<param_list>": [
        ("<type> <identifier>",               opts(prob=0.50)),
        ("<type> <identifier>, <param_list>", opts(prob=0.50)),
    ],

    # -------------------------------------------------
    # STATEMENTS
    # -------------------------------------------------
    "<stmt_list>": [
        ("",                   opts(prob=0.25)),
        ("<stmt>\n<stmt_list>", opts(prob=0.75)),
    ],

    "<stmt>": [
        ("<decl_stmt>;",        opts(prob=0.05)),
        ("<assign_stmt>;",      opts(prob=0.05)),
        ("<if_stmt>",           opts(prob=0.08)),
        ("<while_stmt>",        opts(prob=0.08)),
        ("<for_stmt>",          opts(prob=0.08)),
        ("<switch_stmt>",       opts(prob=0.08)),
        ("asm(\"<asm_instr>\");", opts(prob=0.15)),
        ("<fp_stmt>;",          opts(prob=0.10)),
        ("<fp_complex_stmt>;",  opts(prob=0.08)),
        ("<extern_call_stmt>;", opts(prob=0.07)),
        ("<struct_stmt>;",      opts(prob=0.04)),
        ("<heavy_loop_stmt>;",  opts(prob=0.08)),
        ("<return_stmt>;",      opts(prob=0.02)),
        ("break;",              opts(prob=0.02)),
        ("continue;",           opts(prob=0.02)),
    ],

    "<decl_stmt>": [
        ("<type> <identifier>",                opts(prob=0.10)),
        ("<type> <identifier> = <expr>",       opts(prob=0.25)),
        ("<type> <identifier>, <identifier>",  opts(prob=0.25)),
        ("<type> <identifier>[<int_literal>]", opts(prob=0.40)),
    ],

    "<assign_stmt>": [
        ("<identifier> = <expr>",               opts(prob=0.30)),
        ("<identifier> += <expr>",              opts(prob=0.25)),
        ("<identifier> -= <expr>",              opts(prob=0.15)),
        ("<identifier> *= <expr>",              opts(prob=0.15)),
        ("<identifier>[<expr>] = <expr>",       opts(prob=0.15)),
    ],

    "<if_stmt>": [
        ("if (<expr>) <stmt>",             opts(prob=0.50)),
        ("if (<expr>) <stmt> else <stmt>", opts(prob=0.50)),
    ],

    "<while_stmt>": [
        ("while (<expr>) <stmt>", opts(prob=1.0)),
    ],

    "<for_stmt>": [
        ("for (<assign_stmt>; <expr>; <assign_stmt>) <stmt>", opts(prob=1.0)),
    ],

    "<switch_stmt>": [
        ("switch(<expr>) { <rich_case_list> }", opts(prob=1.0)),
    ],

    "<rich_case_list>": [
        ("case 0: <stmt_list> break;\n"
         "case 1: <stmt_list> break;\n"
         "case 2: <stmt_list> break;\n"
         "case 3: <stmt_list> break;\n"
         "default: <stmt_list> break;",
         opts(prob=1.0)),
    ],

    "<return_stmt>": [
        ("return",        opts(prob=0.5)),
        ("return <expr>", opts(prob=0.5)),
    ],

    # -------------------------------------------------
    # SPECIAL STATEMENTS
    # -------------------------------------------------
    "<extern_call_stmt>": [
        ("extern int printf(const char*, ...); printf(\"%d %d %d\n\", <expr>, <expr>, <expr>)",
         opts(prob=0.5)),
        ("extern int puts(const char*); puts(\"hello from tcc\")",
         opts(prob=0.3)),
        ("extern int abs(int); abs(<int_literal>)",
         opts(prob=0.2)),
    ],

    "<fp_stmt>": [
        ("int (*fp_local)(int) = <identifier>; int r_local = fp_local(<int_literal>);",
         opts(prob=0.60)),
        ("int (*ops[3])(int) = { <identifier>, <identifier>, <identifier> }; "
         "int r2 = ops[1](<int_literal>);",
         opts(prob=0.40)),
    ],

    "<fp_complex_stmt>": [
        ("int (*fpA)(int) = <identifier>; int (*fpB)(int) = fpA; "
         "int res1 = fpB(<int_literal>);",
         opts(prob=0.60)),
        ("int (*table[3])(int) = { <identifier>, <identifier>, <identifier> }; "
         "int res2 = table[2](<int_literal>);",
         opts(prob=0.40)),
    ],

    "<struct_stmt>": [
        ("struct S s; s.a = <int_literal>; s.b = <float_literal>;", opts(prob=0.60)),
        ("union U u; u.x = <int_literal>;",                         opts(prob=0.40)),
    ],

    "<heavy_loop_stmt>": [
        ("for (int i = 0; i < 200; i++) { x += i; if (x & 1) y += x; else y -= x; }",
         opts(prob=1.0)),
    ],

    # -------------------------------------------------
    # EXPRESSIONS
    # -------------------------------------------------
    "<expr>": [
        ("<identifier>",    opts(prob=0.06)),
        ("<int_literal>",   opts(prob=0.20)),
        ("<hex_literal>",   opts(prob=0.08)),
        ("<float_literal>", opts(prob=0.06)),
        ("<char_literal>",  opts(prob=0.04)),
        ("<string_literal>",opts(prob=0.04)),
        ("(<expr>)",        opts(prob=0.06)),
        ("<binary_expr>",   opts(prob=0.20)),
        ("<unary_expr>",    opts(prob=0.06)),
        ("<cond_expr>",     opts(prob=0.06)),
        ("<cast_expr>",     opts(prob=0.04)),
        ("<sizeof_expr>",   opts(prob=0.04)),
        ("<array_access>",  opts(prob=0.03)),
        ("<function_call>", opts(prob=0.03)),
    ],

    "<cond_expr>": [
        ("<expr> ? <expr> : <expr>", opts(prob=1.0)),
    ],

    "<array_access>": [
        ("<identifier>[<expr>]", opts(prob=1.0)),
    ],

    "<cast_expr>": [
        ("(<type>) <expr>",           opts(prob=0.40)),
        ("((long long) <expr>)",      opts(prob=0.35)),
        ("((unsigned short) <expr>)", opts(prob=0.25)),
    ],

    "<sizeof_expr>": [
        ("sizeof(<type>)",       opts(prob=0.5)),
        ("sizeof(<identifier>)", opts(prob=0.5)),
    ],

    "<binary_expr>": [
        ("<expr> + <expr>",  opts(prob=0.08)),
        ("<expr> - <expr>",  opts(prob=0.08)),
        ("<expr> * <expr>",  opts(prob=0.08)),
        ("<expr> / <expr>",  opts(prob=0.08)),
        ("<expr> % <expr>",  opts(prob=0.08)),
        ("<expr> == <expr>", opts(prob=0.08)),
        ("<expr> != <expr>", opts(prob=0.08)),
        ("<expr> > <expr>",  opts(prob=0.08)),
        ("<expr> < <expr>",  opts(prob=0.08)),
        ("<expr> >= <expr>", opts(prob=0.07)),
        ("<expr> <= <expr>", opts(prob=0.07)),
        ("<expr> && <expr>", opts(prob=0.07)),
        ("<expr> || <expr>", opts(prob=0.07)),
    ],

    "<unary_expr>": [
        ("-<expr>",        opts(prob=0.20)),
        ("!<expr>",        opts(prob=0.20)),
        ("+<expr>",        opts(prob=0.10)),
        ("++<identifier>", opts(prob=0.15)),
        ("--<identifier>", opts(prob=0.15)),
        ("<identifier>++", opts(prob=0.10)),
        ("<identifier>--", opts(prob=0.10)),
    ],

    "<function_call>": [
        ("<identifier>()",           opts(prob=0.40)),
        ("<identifier>(<arg_list>)", opts(prob=0.60)),
    ],

    "<arg_list>": [
        ("<expr>",             opts(prob=0.50)),
        ("<expr>, <arg_list>", opts(prob=0.50)),
    ],

    # -------------------------------------------------
    # LITERALS
    # -------------------------------------------------
    "<int_literal>": [
        ("1",           opts(prob=0.03)),
        ("42",          opts(prob=0.03)),
        ("999999999",   opts(prob=0.20)),
        ("2147483647",  opts(prob=0.20)),
        ("4294967295",  opts(prob=0.18)),
        ("1U",          opts(prob=0.10)),
        ("10LL",        opts(prob=0.10)),
        ("0xFFUL",      opts(prob=0.08)),
        ("0b1010",      opts(prob=0.04)),
        ("0777",        opts(prob=0.04)),
    ],

    "<hex_literal>": [
        ("0x1",  opts(prob=0.25)),
        ("0x2A", opts(prob=0.25)),
        ("0x10", opts(prob=0.25)),
        ("0xFF", opts(prob=0.25)),
    ],

    "<float_literal>": [
        ("0.1",    opts(prob=0.30)),
        ("1.5",    opts(prob=0.30)),
        ("3.1415", opts(prob=0.40)),
    ],

    "<char_literal>": [
        ("'a'",   opts(prob=0.15)),
        ("'b'",   opts(prob=0.15)),
        ("'c'",   opts(prob=0.15)),
        ("'x'",   opts(prob=0.10)),
        ("'y'",   opts(prob=0.10)),
        ("'z'",   opts(prob=0.10)),
        ("'\\n'", opts(prob=0.12)),
        ("'\\t'", opts(prob=0.13)),
    ],

    "<string_literal>": [
        ("\"hello\"",          opts(prob=0.20)),
        ("\"abc\"",            opts(prob=0.15)),
        ("\"hello\\nworld\"",  opts(prob=0.25)),
        ("\"tab\\tindent\"",   opts(prob=0.20)),
        ("\"quote\\\"inside\"",opts(prob=0.20)),
    ],

    # -------------------------------------------------
    # INLINE ASM
    # -------------------------------------------------
    "<asm_instr>": [
        ("ldr <reg>, [<reg>, #<int_literal>]", opts(prob=0.25)),
        ("str <reg>, [<reg>, #<int_literal>]", opts(prob=0.25)),
        ("strb <wreg>, [<reg>]",              opts(prob=0.10)),
        ("ldrb <wreg>, [<reg>]",              opts(prob=0.10)),
        ("fadd d0, d1, d2",                   opts(prob=0.10)),
        ("fmul d3, d4, d5",                   opts(prob=0.10)),
        ("b.eq label",                        opts(prob=0.05)),
        ("add <reg>, <reg>, <reg>",           opts(prob=0.03)),
        ("mul <reg>, <reg>, <reg>",           opts(prob=0.02)),
    ],

    "<reg>": [
        ("x0",  opts(prob=1.0 / 32.0)), ("x1",  opts(prob=1.0 / 32.0)),
        ("x2",  opts(prob=1.0 / 32.0)), ("x3",  opts(prob=1.0 / 32.0)),
        ("x4",  opts(prob=1.0 / 32.0)), ("x5",  opts(prob=1.0 / 32.0)),
        ("x6",  opts(prob=1.0 / 32.0)), ("x7",  opts(prob=1.0 / 32.0)),
        ("x8",  opts(prob=1.0 / 32.0)), ("x9",  opts(prob=1.0 / 32.0)),
        ("x10", opts(prob=1.0 / 32.0)), ("x11", opts(prob=1.0 / 32.0)),
        ("x12", opts(prob=1.0 / 32.0)), ("x13", opts(prob=1.0 / 32.0)),
        ("x14", opts(prob=1.0 / 32.0)), ("x15", opts(prob=1.0 / 32.0)),
        ("x16", opts(prob=1.0 / 32.0)), ("x17", opts(prob=1.0 / 32.0)),
        ("x18", opts(prob=1.0 / 32.0)), ("x19", opts(prob=1.0 / 32.0)),
        ("x20", opts(prob=1.0 / 32.0)), ("x21", opts(prob=1.0 / 32.0)),
        ("x22", opts(prob=1.0 / 32.0)), ("x23", opts(prob=1.0 / 32.0)),
        ("x24", opts(prob=1.0 / 32.0)), ("x25", opts(prob=1.0 / 32.0)),
        ("x26", opts(prob=1.0 / 32.0)), ("x27", opts(prob=1.0 / 32.0)),
        ("x28", opts(prob=1.0 / 32.0)), ("x29", opts(prob=1.0 / 32.0)),
        ("x30", opts(prob=1.0 / 32.0)), ("sp",  opts(prob=1.0 / 32.0)),
    ],

    "<wreg>": [
        ("w0",  opts(prob=1.0 / 32.0)), ("w1",  opts(prob=1.0 / 32.0)),
        ("w2",  opts(prob=1.0 / 32.0)), ("w3",  opts(prob=1.0 / 32.0)),
        ("w4",  opts(prob=1.0 / 32.0)), ("w5",  opts(prob=1.0 / 32.0)),
        ("w6",  opts(prob=1.0 / 32.0)), ("w7",  opts(prob=1.0 / 32.0)),
        ("w8",  opts(prob=1.0 / 32.0)), ("w9",  opts(prob=1.0 / 32.0)),
        ("w10", opts(prob=1.0 / 32.0)), ("w11", opts(prob=1.0 / 32.0)),
        ("w12", opts(prob=1.0 / 32.0)), ("w13", opts(prob=1.0 / 32.0)),
        ("w14", opts(prob=1.0 / 32.0)), ("w15", opts(prob=1.0 / 32.0)),
        ("w16", opts(prob=1.0 / 32.0)), ("w17", opts(prob=1.0 / 32.0)),
        ("w18", opts(prob=1.0 / 32.0)), ("w19", opts(prob=1.0 / 32.0)),
        ("w20", opts(prob=1.0 / 32.0)), ("w21", opts(prob=1.0 / 32.0)),
        ("w22", opts(prob=1.0 / 32.0)), ("w23", opts(prob=1.0 / 32.0)),
        ("w24", opts(prob=1.0 / 32.0)), ("w25", opts(prob=1.0 / 32.0)),
        ("w26", opts(prob=1.0 / 32.0)), ("w27", opts(prob=1.0 / 32.0)),
        ("w28", opts(prob=1.0 / 32.0)), ("w29", opts(prob=1.0 / 32.0)),
        ("w30", opts(prob=1.0 / 32.0)), ("wzr", opts(prob=1.0 / 32.0)),
    ],

    # -------------------------------------------------
    # IDENTIFIERS
    # -------------------------------------------------
    "<identifier>": [
        ("x",     opts(prob=0.10)),
        ("y",     opts(prob=0.10)),
        ("z",     opts(prob=0.10)),
        ("a",     opts(prob=0.08)),
        ("b",     opts(prob=0.08)),
        ("c",     opts(prob=0.08)),
        ("foo",   opts(prob=0.10)),
        ("bar",   opts(prob=0.10)),
        ("baz",   opts(prob=0.08)),
        ("temp",  opts(prob=0.08)),
        ("value", opts(prob=0.05)),
        ("index", opts(prob=0.05)),
    ],
}

Seeds = project_evaluation.get_seeds()
Fuzzer = None
mut = Mutator()
ps = PowerSchedule()
 
def yield_next_input() -> Generator[bytes, None, None]:
    # Implement your fuzzer here
    # The fuzzer will exit when no more inputs are yielded
    # So you probably want to yield an uncapped number of inputs
    # make sure to yield bytes, not strings; use .encode() to convert a string to bytes
    PROB_GRAMMAR_FUZZER = ProbabilisticGrammarFuzzer(grammar=C_GRAMMAR, start_symbol="<start>", max_nonterminals=100)
    MUTATION_COVERAGE_FUZZER = MutationFuzzer(Seeds)
    if Seeds  : 
         #FUZZ = MUTATION_COVERAGE_FUZZER
         # FUZZ = AdvancedMutationFuzzer(Seeds, mut, ps)
          FUZZ = GreyboxFuzzer(Seeds, mut, ps)
    else:
          FUZZ = PROB_GRAMMAR_FUZZER

    while True:
          program = FUZZ.fuzz()
          yield program.encode("utf-8")
