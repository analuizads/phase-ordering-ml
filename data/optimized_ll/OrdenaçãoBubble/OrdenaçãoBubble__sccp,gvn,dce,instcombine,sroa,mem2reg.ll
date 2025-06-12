; ModuleID = 'data/original_ll/OrdenaçãoBubble.ll'
source_filename = "data/c_codes/Ordena\C3\A7\C3\A3oBubble.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@__const.main.v = private unnamed_addr constant [5 x i32] [i32 5, i32 3, i32 8, i32 4, i32 2], align 16
@.str = private unnamed_addr constant [4 x i8] c"%d \00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @bubbleSort(ptr noundef %0, i32 noundef %1) #0 {
  br label %3

3:                                                ; preds = %34, %2
  %4 = phi ptr [ %11, %34 ], [ %0, %2 ]
  %5 = phi ptr [ %12, %34 ], [ %0, %2 ]
  %6 = phi i32 [ %35, %34 ], [ 0, %2 ]
  %7 = add nsw i32 %1, -1
  %8 = icmp slt i32 %6, %7
  br i1 %8, label %9, label %36

9:                                                ; preds = %3
  br label %10

10:                                               ; preds = %32, %9
  %storemerge = phi i32 [ 0, %9 ], [ %.pre-phi, %32 ]
  %11 = phi ptr [ %4, %9 ], [ %33, %32 ]
  %12 = phi ptr [ %5, %9 ], [ %33, %32 ]
  %13 = xor i32 %6, -1
  %14 = add i32 %1, %13
  %15 = icmp slt i32 %storemerge, %14
  br i1 %15, label %16, label %34

16:                                               ; preds = %10
  %17 = sext i32 %storemerge to i64
  %18 = getelementptr inbounds i32, ptr %12, i64 %17
  %19 = load i32, ptr %18, align 4
  %20 = add nsw i32 %storemerge, 1
  %21 = sext i32 %20 to i64
  %22 = getelementptr inbounds i32, ptr %11, i64 %21
  %23 = load i32, ptr %22, align 4
  %24 = icmp sgt i32 %19, %23
  br i1 %24, label %25, label %32

25:                                               ; preds = %16
  %26 = getelementptr inbounds i32, ptr %11, i64 %17
  %27 = load i32, ptr %26, align 4
  %28 = load i32, ptr %22, align 4
  store i32 %28, ptr %26, align 4
  %29 = add nsw i32 %storemerge, 1
  %30 = sext i32 %29 to i64
  %31 = getelementptr inbounds i32, ptr %0, i64 %30
  store i32 %27, ptr %31, align 4
  br label %32

32:                                               ; preds = %25, %16
  %.pre-phi = phi i32 [ %29, %25 ], [ %20, %16 ]
  %33 = phi ptr [ %0, %25 ], [ %11, %16 ]
  br label %10, !llvm.loop !6

34:                                               ; preds = %10
  %35 = add nuw nsw i32 %6, 1
  br label %3, !llvm.loop !8

36:                                               ; preds = %3
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca [5 x i32], align 16
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 16 dereferenceable(20) %1, ptr noundef nonnull align 16 dereferenceable(20) @__const.main.v, i64 20, i1 false)
  call void @bubbleSort(ptr noundef nonnull %1, i32 noundef 5)
  br label %2

2:                                                ; preds = %5, %0
  %3 = phi i32 [ %10, %5 ], [ 0, %0 ]
  %4 = icmp samesign ult i32 %3, 5
  br i1 %4, label %5, label %11

5:                                                ; preds = %2
  %6 = zext nneg i32 %3 to i64
  %7 = getelementptr inbounds nuw [5 x i32], ptr %1, i64 0, i64 %6
  %8 = load i32, ptr %7, align 4
  %9 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %8) #3
  %10 = add nuw nsw i32 %3, 1
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
