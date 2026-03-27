
 Expressao 
    LDR R0, =__fc_3_0
    VLDR S0, [R0]
    VPUSH {S0}
    LDR R0, =__fc_2_0
    VLDR S0, [R0]
    VPUSH {S0}
    VPOP {S0}
    VPOP {S1}
    VADD.F32 S0, S1, S0
    VPUSH {S0}
    VPOP {S0}
    LDR R1, =resultado_0
    VSTR S0, [R1]

 Expressao 
    LDR R0, =10
    PUSH {R0}
    LDR R0, =4
    PUSH {R0}
    POP {R1}
    POP {R0}
    SUB R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_1
    STR R0, [R1]

 Expressao 
    LDR R0, =6
    PUSH {R0}
    LDR R0, =7
    PUSH {R0}
    POP {R1}
    POP {R0}
    MUL R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_2
    STR R0, [R1]

 Expressao 
    LDR R0, =__fc_8_0
    VLDR S0, [R0]
    VPUSH {S0}
    LDR R0, =__fc_2_0
    VLDR S0, [R0]
    VPUSH {S0}
    VPOP {S0}
    VPOP {S1}
    VDIV.F32 S0, S1, S0
    VPUSH {S0}
    VPOP {S0}
    LDR R1, =resultado_3
    VSTR S0, [R1]

 Expressao 
    LDR R0, =9
    PUSH {R0}
    LDR R0, =2
    PUSH {R0}
    POP {R1}
    POP {R0}
    SDIV R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_4
    STR R0, [R1]

 Expressao 
    LDR R0, =10
    PUSH {R0}
    LDR R0, =3
    PUSH {R0}
    POP {R1}
    POP {R0}
    SDIV R2, R0, R1
    MUL R2, R2, R1
    SUB R0, R0, R2
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_5
    STR R0, [R1]

 Expressao 
    LDR R0, =2
    PUSH {R0}
    LDR R0, =3
    PUSH {R0}
    POP {R1}
    POP {R0}
    @ POW int: R0 = R0 ^ R1 (loop inline)
    MOV R2, #1
    MOV R3, R1
    CMP R3, #0
    BEQ __pow_done_6
__pow_loop_6:
    MUL R2, R2, R0
    SUBS R3, R3, #1
    BNE __pow_loop_6
__pow_done_6:
    MOV R0, R2
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_6
    STR R0, [R1]

 Expressao 
    LDR R0, =__fc_2_0
    VLDR S0, [R0]
    VPUSH {S0}
    LDR R0, =__fc_3_0
    VLDR S0, [R0]
    VPUSH {S0}
    VPOP {S0}
    VPOP {S1}
    VADD.F32 S0, S1, S0
    VPUSH {S0}
    LDR R0, =__fc_4_0
    VLDR S0, [R0]
    VPUSH {S0}
    LDR R0, =__fc_5_0
    VLDR S0, [R0]
    VPUSH {S0}
    VPOP {S0}
    VPOP {S1}
    VADD.F32 S0, S1, S0
    VPUSH {S0}
    VPOP {S0}
    VPOP {S1}
    VMUL.F32 S0, S1, S0
    VPUSH {S0}
    VPOP {S0}
    LDR R1, =resultado_7
    VSTR S0, [R1]

 Expressao 
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    LDR R0, =__fc_5_0
    VLDR S0, [R0]
    VPUSH {S0}
    @ STORE X
    VPOP {S0}
    LDR R1, =X
    VSTR S0, [R1]
    VPUSH {S0}
    VPOP {S0}
    LDR R1, =resultado_8
    VSTR S0, [R1]

 Expressao 
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    @ LOAD X
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_9
    STR R0, [R1]

 Expressao 
    LDR R0, =0
    PUSH {R0}
    @ RES 0 (float)
    LDR R0, =resultado_0
    VLDR S0, [R0]
    VPUSH {S0}
    VPOP {S0}
    LDR R1, =resultado_10
    VSTR S0, [R1]
