; ModuleID = ""
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32* @"array_of_string"(i8* %".1") 

declare i8* @"string_of_array"(i32* %".1") 

declare i32 @"length_of_string"(i8* %".1") 

declare i8* @"string_of_int"(i32 %".1") 

declare i8* @"string_cat"(i8* %".1", i8* %".2") 

declare void @"print_string"(i8* %".1") 

declare void @"print_int"(i32 %".1") 

declare void @"print_bool"(i32 %".1") 

define i32 @"main"() 
{
entry:
  %"value-3" = alloca i32
  store i32 10, i32* %"value-3"
  br label %"loop_cond"
loop_cond:
  %"value-3.1" = load i32, i32* %"value-3"
  %"greattmp" = icmp sgt i32 %"value-3.1", 0
  br i1 %"greattmp", label %"loop_body", label %"loop_end"
loop_body:
  %".5" = load i32, i32* %"value-3"
  call void @"print_int"(i32 %".5")
  %".6" = getelementptr inbounds [2 x i8], [2 x i8]* @"constant0", i32 0, i32 0
  call void @"print_string"(i8* %".6")
  br label %"loop_cond"
loop_end:
  ret i32 0
}

@"constant0" = global [2 x i8] c"\0a\00"