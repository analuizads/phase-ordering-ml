; ModuleID = 'data/original_ll/OrdenaçãoBubble.ll'
source_filename = "data/c_codes/Ordena\C3\A7\C3\A3oBubble.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@__const.main.v = private unnamed_addr constant [5 x i32] [i32 5, i32 3, i32 8, i32 4, i32 2], align 16
@.str = private unnamed_addr constant [4 x i8] c"%d \00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @bubbleSort(ptr noundef %0, i32 noundef %1) #0 {
  br label %3

3:                                                ; preds = %22, %2
  %.01 = phi i32 [ 0, %2 ], [ %23, %22 ]
  %4 = add nsw i32 %1, -1
  %5 = icmp slt i32 %.01, %4
  br i1 %5, label %6, label %24

6:                                                ; preds = %3
  br label %7

7:                                                ; preds = %21, %6
  %.0 = phi i32 [ 0, %6 ], [ %15, %21 ]
  %8 = xor i32 %.01, -1
  %9 = add i32 %1, %8
  %10 = icmp slt i32 %.0, %9
  br i1 %10, label %11, label %22

11:                                               ; preds = %7
  %12 = zext nneg i32 %.0 to i64
  %13 = getelementptr inbounds nuw i32, ptr %0, i64 %12
  %14 = load i32, ptr %13, align 4
  %15 = add nuw nsw i32 %.0, 1
  %16 = zext nneg i32 %15 to i64
  %17 = getelementptr inbounds nuw i32, ptr %0, i64 %16
  %18 = load i32, ptr %17, align 4
  %19 = icmp sgt i32 %14, %18
  br i1 %19, label %20, label %21

20:                                               ; preds = %11
  store i32 %18, ptr %13, align 4
  store i32 %14, ptr %17, align 4
  br label %21

21:                                               ; preds = %20, %11
  br label %7, !llvm.loop !6

22:                                               ; preds = %7
  %23 = add nuw nsw i32 %.01, 1
  br label %3, !llvm.loop !8

24:                                               ; preds = %3
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca [5 x i32], align 16
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 16 dereferenceable(20) %1, ptr noundef nonnull align 16 dereferenceable(20) @__const.main.v, i64 20, i1 false)
  call void @bubbleSort(ptr noundef nonnull %1, i32 noundef 5)
  br label %2

2:                                                ; preds = %4, %0
  %.0 = phi i32 [ 0, %0 ], [ %9, %4 ]
  %3 = icmp samesign ult i32 %.0, 5
  br i1 %3, label %4, label %10

4:                                                ; preds = %2
  %5 = zext nneg i32 %.0 to i64
  %6 = getelementptr inbounds nuw [5 x i32], ptr %1, i64 0, i64 %5
  %7 = load i32, ptr %6, align 4
  %8 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %7) #3
  %9 = add nuw nsw i32 %.0, 1
  br label %2, !llvm.loop !9

10:                                               ; preds = %2
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
