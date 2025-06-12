; ModuleID = 'data/original_ll/OrdenaçãoBubble.ll'
source_filename = "data/c_codes/Ordena\C3\A7\C3\A3oBubble.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@__const.main.v = private unnamed_addr constant [5 x i32] [i32 5, i32 3, i32 8, i32 4, i32 2], align 16
@.str = private unnamed_addr constant [4 x i8] c"%d \00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @bubbleSort(ptr noundef %0, i32 noundef %1) #0 {
  br label %3

3:                                                ; preds = %29, %2
  %4 = phi ptr [ %0, %2 ], [ %10, %29 ]
  %5 = phi i32 [ 0, %2 ], [ %30, %29 ]
  %6 = add nsw i32 %1, -1
  %7 = icmp slt i32 %5, %6
  br i1 %7, label %8, label %31

8:                                                ; preds = %3
  br label %9

9:                                                ; preds = %26, %8
  %10 = phi ptr [ %4, %8 ], [ %27, %26 ]
  %11 = phi i32 [ 0, %8 ], [ %28, %26 ]
  %12 = xor i32 %5, -1
  %13 = add i32 %1, %12
  %14 = icmp slt i32 %11, %13
  br i1 %14, label %15, label %29

15:                                               ; preds = %9
  %16 = sext i32 %11 to i64
  %17 = getelementptr i32, ptr %10, i64 %16
  %18 = load i32, ptr %17, align 4
  %19 = getelementptr i8, ptr %17, i64 4
  %20 = load i32, ptr %19, align 4
  %21 = icmp sgt i32 %18, %20
  br i1 %21, label %22, label %26

22:                                               ; preds = %15
  %23 = load i32, ptr %19, align 4
  %24 = getelementptr i32, ptr %0, i64 %16
  store i32 %23, ptr %24, align 4
  %25 = getelementptr i8, ptr %24, i64 4
  store i32 %18, ptr %25, align 4
  br label %26

26:                                               ; preds = %22, %15
  %27 = phi ptr [ %0, %22 ], [ %10, %15 ]
  %28 = add nsw i32 %11, 1
  br label %9, !llvm.loop !6

29:                                               ; preds = %9
  %30 = add nsw i32 %5, 1
  br label %3, !llvm.loop !8

31:                                               ; preds = %3
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca [5 x i32], align 16
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 16 dereferenceable(20) %1, ptr noundef nonnull align 16 dereferenceable(20) @__const.main.v, i64 20, i1 false)
  call void @bubbleSort(ptr noundef nonnull %1, i32 noundef 5)
  br label %2

2:                                                ; preds = %5, %0
  %3 = phi i32 [ 0, %0 ], [ %10, %5 ]
  %4 = icmp slt i32 %3, 5
  br i1 %4, label %5, label %11

5:                                                ; preds = %2
  %6 = sext i32 %3 to i64
  %7 = getelementptr inbounds [5 x i32], ptr %1, i64 0, i64 %6
  %8 = load i32, ptr %7, align 4
  %9 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %8) #3
  %10 = add nsw i32 %3, 1
  br label %2, !llvm.loop !9

11:                                               ; preds = %2
  ret i32 0
}

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #1

declare i32 @printf(ptr noundef, ...) #2

attributes #0 = { noinline nounwind uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #2 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind }

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
!8 = distinct !{!8, !7}
!9 = distinct !{!9, !7}
