; ModuleID = 'data/original_ll/FibonacciIterativo.ll'
source_filename = "data/c_codes/FibonacciIterativo.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [4 x i8] c"%d \00", align 1
@.str.1 = private unnamed_addr constant [12 x i8] c"Fibonacci: \00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @fibonacci(i32 noundef %0) #0 {
  br label %2

2:                                                ; preds = %4, %1
  %.09 = phi i32 [ 1, %1 ], [ %6, %4 ]
  %.08 = phi i32 [ 0, %1 ], [ %.09, %4 ]
  %.0 = phi i32 [ 0, %1 ], [ %7, %4 ]
  %3 = icmp slt i32 %.0, %0
  br i1 %3, label %4, label %8

4:                                                ; preds = %2
  %5 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %.08) #2
  %6 = add nsw i32 %.08, %.09
  %7 = add nuw nsw i32 %.0, 1
  br label %2, !llvm.loop !6

8:                                                ; preds = %2
  ret void
}

declare i32 @printf(ptr noundef, ...) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str.1) #2
  call void @fibonacci(i32 noundef 10)
  ret i32 0
}

attributes #0 = { noinline nounwind uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 2}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 20.1.2 (0ubuntu1)"}
!6 = distinct !{!6, !7}
!7 = !{!"llvm.loop.mustprogress"}
