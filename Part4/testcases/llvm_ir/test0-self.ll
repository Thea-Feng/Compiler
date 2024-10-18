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
  %"str-3" = alloca [13 x i8]
  store [13 x i8] c"hello world!\00", [13 x i8]* %"str-3"
  %".3" = getelementptr inbounds [13 x i8], [13 x i8]* %"str-3", i32 0, i32 0
  call void @"print_string"(i8* %".3")
  ret i32 0
}
