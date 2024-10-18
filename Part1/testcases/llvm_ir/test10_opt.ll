; ModuleID = './llvm_ir/test10.ll'
source_filename = "./llvm_ir/test10.ll"

; Function Attrs: nofree nounwind
declare i32 @printf(i8* nocapture readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare i32 @scanf(i8* nocapture readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
define i32 @main() local_unnamed_addr #0 {
  %C = alloca i32, align 4
  %D = alloca i32, align 4
  %_scanf_format_1 = alloca [6 x i8], align 1
  %.fca.0.gep5 = getelementptr inbounds [6 x i8], [6 x i8]* %_scanf_format_1, i64 0, i64 0
  store i8 37, i8* %.fca.0.gep5, align 1
  %.fca.1.gep6 = getelementptr inbounds [6 x i8], [6 x i8]* %_scanf_format_1, i64 0, i64 1
  store i8 100, i8* %.fca.1.gep6, align 1
  %.fca.2.gep7 = getelementptr inbounds [6 x i8], [6 x i8]* %_scanf_format_1, i64 0, i64 2
  store i8 32, i8* %.fca.2.gep7, align 1
  %.fca.3.gep8 = getelementptr inbounds [6 x i8], [6 x i8]* %_scanf_format_1, i64 0, i64 3
  store i8 37, i8* %.fca.3.gep8, align 1
  %.fca.4.gep = getelementptr inbounds [6 x i8], [6 x i8]* %_scanf_format_1, i64 0, i64 4
  store i8 100, i8* %.fca.4.gep, align 1
  %.fca.5.gep = getelementptr inbounds [6 x i8], [6 x i8]* %_scanf_format_1, i64 0, i64 5
  store i8 0, i8* %.fca.5.gep, align 1
  %1 = call i32 (i8*, ...) @scanf(i8* nonnull %.fca.0.gep5, i32* nonnull %C, i32* nonnull %D)
  %_tmp_1 = load i32, i32* %C, align 4
  %_tmp_2 = load i32, i32* %D, align 4
  %factor = shl i32 %_tmp_1, 1
  %_tmp_8 = add i32 %_tmp_2, -26
  %_tmp_10 = add i32 %_tmp_8, %factor
  %_printf_format_1 = alloca [4 x i8], align 1
  %.fca.0.gep1 = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_1, i64 0, i64 0
  store i8 37, i8* %.fca.0.gep1, align 1
  %.fca.1.gep2 = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_1, i64 0, i64 1
  store i8 100, i8* %.fca.1.gep2, align 1
  %.fca.2.gep3 = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_1, i64 0, i64 2
  store i8 10, i8* %.fca.2.gep3, align 1
  %.fca.3.gep4 = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_1, i64 0, i64 3
  store i8 0, i8* %.fca.3.gep4, align 1
  %2 = call i32 (i8*, ...) @printf(i8* nonnull %.fca.0.gep1, i32 %_tmp_10)
  %_tmp_13 = load i32, i32* %D, align 4
  %_tmp_16 = sub i32 16, %_tmp_13
  %_printf_format_2 = alloca [4 x i8], align 1
  %.fca.0.gep = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_2, i64 0, i64 0
  store i8 37, i8* %.fca.0.gep, align 1
  %.fca.1.gep = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_2, i64 0, i64 1
  store i8 100, i8* %.fca.1.gep, align 1
  %.fca.2.gep = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_2, i64 0, i64 2
  store i8 10, i8* %.fca.2.gep, align 1
  %.fca.3.gep = getelementptr inbounds [4 x i8], [4 x i8]* %_printf_format_2, i64 0, i64 3
  store i8 0, i8* %.fca.3.gep, align 1
  %3 = call i32 (i8*, ...) @printf(i8* nonnull %.fca.0.gep, i32 %_tmp_16)
  ret i32 0
}

attributes #0 = { nofree nounwind }
