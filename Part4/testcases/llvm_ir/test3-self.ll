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
  %"y-3" = alloca i32
  store i32 5, i32* %"y-3"
  %".3" = load i32, i32* %"y-3"
  call void @"print_int"(i32 %".3")
  %".4" = getelementptr inbounds [2 x i8], [2 x i8]* @"constant0", i32 0, i32 0
  call void @"print_string"(i8* %".4")
  %"y-3.1" = load i32, i32* %"y-3"
  %"greattmp" = icmp sgt i32 %"y-3.1", 0
  br i1 %"greattmp", label %"if_block", label %"else_block"
if_block:
  %"is_y_positive-4" = alloca i32
  store i32 1, i32* %"is_y_positive-4"
  %".7" = load i32, i32* %"is_y_positive-4"
  call void @"print_bool"(i32 %".7")
  br label %"merge_block"
else_block:
  %"is_y_positive-5" = alloca i32
  store i32 0, i32* %"is_y_positive-5"
  %".10" = load i32, i32* %"is_y_positive-5"
  call void @"print_bool"(i32 %".10")
  br label %"merge_block"
merge_block:
  ret i32 0
}

@"constant0" = global [2 x i8] c"\0a\00"