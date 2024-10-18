; Declare printf
declare i32 @printf(i8*, ...)

; Declare scanf
declare i32 @scanf(i8*, ...)

define i32 @main() {
	%A = alloca i32
	store i32 10, i32* %A
	%B = alloca i32
	store i32 20, i32* %B
	%C = alloca i32
	%D = alloca i32
	%_scanf_format_1 = alloca [6 x i8]
	store [6 x i8] c"%d %d\00", [6 x i8]* %_scanf_format_1
	%_scanf_str_1 = getelementptr [6 x i8], [6 x i8]* %_scanf_format_1, i32 0, i32 0
	call i32 (i8*, ...) @scanf(i8* %_scanf_str_1, i32* %C, i32* %D)
	%_tmp_1 = load i32, i32* %C
	%_tmp_2 = load i32, i32* %D
	%_tmp_3 = load i32, i32* %A
	%_tmp_4 = sub i32 %_tmp_2, %_tmp_3
	%_tmp_5 = add i32 %_tmp_4, 4
	%_tmp_6 = add i32 %_tmp_1, %_tmp_5
	%_tmp_7 = load i32, i32* %B
	%_tmp_8 = sub i32 %_tmp_6, %_tmp_7
	%_tmp_9 = load i32, i32* %C
	%_tmp_10 = add i32 %_tmp_8, %_tmp_9
	%_printf_format_1 = alloca [4 x i8]
	store [4 x i8] c"%d\0A\00", [4 x i8]* %_printf_format_1
	%_printf_str_1 = getelementptr [4 x i8], [4 x i8]* %_printf_format_1, i32 0, i32 0
	call i32 (i8*, ...) @printf(i8* %_printf_str_1, i32 %_tmp_10)
	%_tmp_11 = load i32, i32* %A
	%_tmp_12 = add i32 %_tmp_11, 5
	%_tmp_13 = load i32, i32* %D
	%_tmp_14 = sub i32 3, 2
	%_tmp_15 = sub i32 %_tmp_13, %_tmp_14
	%_tmp_16 = sub i32 %_tmp_12, %_tmp_15
	%_printf_format_2 = alloca [4 x i8]
	store [4 x i8] c"%d\0A\00", [4 x i8]* %_printf_format_2
	%_printf_str_2 = getelementptr [4 x i8], [4 x i8]* %_printf_format_2, i32 0, i32 0
	call i32 (i8*, ...) @printf(i8* %_printf_str_2, i32 %_tmp_16)
	%_tmp_17 = load i32, i32* %C
	%_tmp_18 = add i32 %_tmp_17, 20
	store i32 %_tmp_18, i32* %D
	ret i32 0
}
