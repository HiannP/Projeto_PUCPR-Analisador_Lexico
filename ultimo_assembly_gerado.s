.data
    f_3_5: .double 3.5
    f_2_5: .double 2.5
    f_5_0: .double 5.0
    f_4_0: .double 4.0
    f_2_0: .double 2.0
    resultado_0: .word 0
    resultado_1: .word 0
    resultado_2: .word 0
    resultado_3: .word 0
    resultado_4: .word 0
    resultado_5: .word 0
    resultado_6: .word 0
    resultado_7: .double 0.0
    resultado_8: .double 0.0
    resultado_9: .word 0
    X: .word 0
    resultado_10: .word 0
    Y: .word 0
    resultado_11: .word 0
    resultado_12: .word 0
    resultado_13: .word 0
    resultado_14: .word 0
    resultado_15: .word 0
    resultado_16: .word 0
    resultado_17: .double 0.0

.text
.global _start
_start:

    @ Expressao
    LDR R0, =3
    PUSH {R0}
    LDR R0, =4
    PUSH {R0}
    POP {R1}
    POP {R0}
    ADD R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_0
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =10
    PUSH {R0}
    LDR R0, =2
    PUSH {R0}
    POP {R1}
    POP {R0}
    SUB R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_1
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
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
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =20
    PUSH {R0}
    LDR R0, =5
    PUSH {R0}
    POP {R1}
    POP {R0}
    MOV R2, #0
loop_div_1:
    CMP R0, R1
    BLT end_div_1
    SUB R0, R0, R1
    ADD R2, R2, #1
    B loop_div_1
end_div_1:
    MOV R0, R2
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_3
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =20
    PUSH {R0}
    LDR R0, =6
    PUSH {R0}
    POP {R1}
    POP {R0}
    MOV R2, #0
loop_div_2:
    CMP R0, R1
    BLT end_div_2
    SUB R0, R0, R1
    ADD R2, R2, #1
    B loop_div_2
end_div_2:
    MOV R0, R2
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_4
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =20
    PUSH {R0}
    LDR R0, =6
    PUSH {R0}
    POP {R1}
    POP {R0}
loop_mod_3:
    CMP R0, R1
    BLT end_mod_3
    SUB R0, R0, R1
    B loop_mod_3
end_mod_3:
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_5
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =2
    PUSH {R0}
    LDR R0, =5
    PUSH {R0}
    POP {R1}
    POP {R0}
    MOV R2, #1
loop_pow_4:
    CMP R1, #0
    BEQ end_pow_4
    MUL R2, R2, R0
    SUB R1, R1, #1
    B loop_pow_4
end_pow_4:
    MOV R0, R2
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_6
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =f_3_5
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =f_2_5
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    VPOP {D1}
    VADD.F64 D0, D1, D0
    VPUSH {D0}
    VPOP {D0}
    LDR R1, =resultado_7
    VSTR D0, [R1]
    LDR R2, =0xFF200020
    VMOV R0, S0
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =f_5_0
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =2
    PUSH {R0}
    POP {R0}
    VMOV S0, R0
    VCVT.F64.S32 D0, S0
    VPOP {D1}
    VMUL.F64 D0, D1, D0
    VPUSH {D0}
    VPOP {D0}
    LDR R1, =resultado_8
    VSTR D0, [R1]
    LDR R2, =0xFF200020
    VMOV R0, S0
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =2
    PUSH {R0}
    LDR R0, =3
    PUSH {R0}
    POP {R1}
    POP {R0}
    ADD R0, R0, R1
    PUSH {R0}
    LDR R0, =4
    PUSH {R0}
    LDR R0, =5
    PUSH {R0}
    POP {R1}
    POP {R0}
    MUL R0, R0, R1
    PUSH {R0}
    POP {R1}
    POP {R0}
    MUL R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_9
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_10
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =Y
    LDR R0, [R0]
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_11
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_12
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_13
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    LDR R0, =X
    LDR R0, [R0]
    PUSH {R0}
    POP {R1}
    POP {R0}
    ADD R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_14
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =2
    PUSH {R0}
    LDR R0, =3
    PUSH {R0}
    POP {R1}
    POP {R0}
    ADD R0, R0, R1
    PUSH {R0}
    LDR R0, =4
    PUSH {R0}
    LDR R0, =5
    PUSH {R0}
    LDR R0, =2
    PUSH {R0}
    POP {R1}
    POP {R0}
    MUL R0, R0, R1
    PUSH {R0}
    POP {R1}
    POP {R0}
    ADD R0, R0, R1
    PUSH {R0}
    POP {R1}
    POP {R0}
    MUL R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_15
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =10
    PUSH {R0}
    LDR R0, =2
    PUSH {R0}
    POP {R1}
    POP {R0}
    MOV R2, #0
loop_div_5:
    CMP R0, R1
    BLT end_div_5
    SUB R0, R0, R1
    ADD R2, R2, #1
    B loop_div_5
end_div_5:
    MOV R0, R2
    PUSH {R0}
    LDR R0, =3
    PUSH {R0}
    LDR R0, =1
    PUSH {R0}
    POP {R1}
    POP {R0}
    ADD R0, R0, R1
    PUSH {R0}
    POP {R1}
    POP {R0}
    MUL R0, R0, R1
    PUSH {R0}
    POP {R0}
    LDR R1, =resultado_16
    STR R0, [R1]
    LDR R2, =0xFF200020
    AND R0, R0, #0xF
    STR R0, [R2]

    @ Expressao
    LDR R0, =f_2_5
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =f_3_5
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    VPOP {D1}
    VADD.F64 D0, D1, D0
    VPUSH {D0}
    LDR R0, =f_4_0
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =f_2_0
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    VPOP {D1}
    VMUL.F64 D0, D1, D0
    VPUSH {D0}
    VPOP {D0}
    VPOP {D1}
    VDIV.F64 D0, D1, D0
    VPUSH {D0}
    VPOP {D0}
    LDR R1, =resultado_17
    VSTR D0, [R1]
    LDR R2, =0xFF200020
    VMOV R0, S0
    AND R0, R0, #0xF
    STR R0, [R2]

end:
    B end
