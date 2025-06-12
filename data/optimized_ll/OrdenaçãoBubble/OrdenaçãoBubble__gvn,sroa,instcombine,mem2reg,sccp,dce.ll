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
  %4 = phi i32 [ %30, %29 ], [ 0, %2 ]
  %5 = add nsw i32 %1, -1
  %6 = icmp slt i32 %4, %5
  br i1 %6, label %7, label %31

7:                                                ; preds = %3
  br label %8

8:                                                ; preds = %28, %7
  %.0 = phi i32 [ 0, %7 ], [ %.pre-phi, %28 ]
  %9 = xor i32 %4, -1
  %10 = add i32 %1, %9
  %11 = icmp slt i32 %.0, %10
  br i1 %11, label %12, label %29

12:                                               ; preds = %8
  %13 = sext i32 %.0 to i64
  %14 = getelementptr inbounds i32, ptr %0, i64 %13
  %15 = load i32, ptr %14, align 4
  %16 = add nsw i32 %.0, 1
  %17 = sext i32 %16 to i64
  %18 = getelementptr inbounds i32, ptr %0, i64 %17
  %19 = load i32, ptr %18, align 4
  %20 = icmp sgt i32 %15, %19
  br i1 %20, label %21, label %28

21:                                               ; preds = %12
  %22 = getelementptr inbounds i32, ptr %0, i64 %13
  %23 = load i32, ptr %22, align 4
  %24 = load i32, ptr %18, align 4
  store i32 %24, ptr %22, align 4
  %25 = add nsw i32 %.0, 1
  %26 = sext i32 %25 to i64
  %27 = getelementptr inbounds i32, ptr %0, i64 %26
  store i32 %23, ptr %27, align 4
  br label %28

28:                                               ; preds = %21, %12
  %.pre-phi = phi i32 [ %25, %21 ], [ %16, %12 ]
  br label %8, !llvm.loop !6

29:                                               ; preds = %8
  %30 = add nuw nsw i32 %4, 1
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
