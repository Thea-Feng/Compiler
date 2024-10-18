	.text
	.file	"test5.ll"
	.globl	main                    # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
# %bb.0:
	addi	sp, sp, -48
	sd	ra, 40(sp)
	sd	s0, 32(sp)
	sd	s1, 24(sp)
	sd	s2, 16(sp)
	addi	s0, zero, 37
	sb	s0, 9(sp)
	addi	s1, zero, 100
	sb	s1, 10(sp)
	sb	zero, 11(sp)
	addi	a0, sp, 9
	addi	a1, sp, 12
	call	scanf
	lw	a0, 12(sp)
	addi	a1, zero, 10
	addi	s2, zero, 10
	call	__muldi3
	addi	a1, a0, 45
	sb	s0, 5(sp)
	sb	s1, 6(sp)
	sb	s2, 7(sp)
	sb	zero, 8(sp)
	addi	a0, sp, 5
	call	printf
	mv	a0, zero
	ld	s2, 16(sp)
	ld	s1, 24(sp)
	ld	s0, 32(sp)
	ld	ra, 40(sp)
	addi	sp, sp, 48
	ret
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
