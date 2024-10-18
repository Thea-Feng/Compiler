	.text
	.file	"test10.ll"
	.globl	main                    # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
# %bb.0:
	addi	sp, sp, -64
	sd	ra, 56(sp)
	sd	s0, 48(sp)
	sd	s1, 40(sp)
	sd	s2, 32(sp)
	addi	s0, zero, 37
	sb	s0, 18(sp)
	addi	s1, zero, 100
	sb	s1, 19(sp)
	addi	a0, zero, 32
	sb	a0, 20(sp)
	sb	s0, 21(sp)
	sb	s1, 22(sp)
	sb	zero, 23(sp)
	addi	a0, sp, 18
	addi	a1, sp, 28
	addi	a2, sp, 24
	call	scanf
	lw	a0, 28(sp)
	lw	a1, 24(sp)
	slli	a0, a0, 1
	addw	a0, a1, a0
	addi	a1, a0, -26
	sb	s0, 14(sp)
	sb	s1, 15(sp)
	addi	s2, zero, 10
	sb	s2, 16(sp)
	sb	zero, 17(sp)
	addi	a0, sp, 14
	call	printf
	lw	a0, 24(sp)
	addi	a1, zero, 16
	subw	a1, a1, a0
	sb	s0, 10(sp)
	sb	s1, 11(sp)
	sb	s2, 12(sp)
	sb	zero, 13(sp)
	addi	a0, sp, 10
	call	printf
	mv	a0, zero
	ld	s2, 32(sp)
	ld	s1, 40(sp)
	ld	s0, 48(sp)
	ld	ra, 56(sp)
	addi	sp, sp, 64
	ret
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
