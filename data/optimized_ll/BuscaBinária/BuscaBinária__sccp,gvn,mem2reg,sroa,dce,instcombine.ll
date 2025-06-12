; ModuleID = 'data/original_ll/BuscaBinária.ll'
source_filename = "data/c_codes/BuscaBin\C3\A1ria.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@__const.main.v = private unnamed_addr constant [5 x i32] [i32 1, i32 3, i32 5, i32 7, i32 9], align 16
@.str = private unnamed_addr constant [15 x i8] c"Posi\C3\A7\C3\A3o: %d\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @buscaBinaria(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = add nsw i32 %1, -1
  br label %5

5:                                                ; preds = %22, %3
  %6 = phi i32 [ %23, %22 ], [ %4, %3 ]
  %7 = phi i32 [ %24, %22 ], [ 0, %3 ]
  %.not = icmp sgt i32 %7, %6
  br i1 %.not, label %25, label %8

8:                                                ; preds = %5
  %9 = add nsw i32 %7, %6
  %10 = sdiv i32 %9, 2
  %11 = sext i32 %10 to i64
  %12 = getelementptr inbounds i32, ptr %0, i64 %11
  %13 = load i32, ptr %12, align 4
  %14 = icmp eq i32 %13, %2
  br i1 %14, label %15, label %16

15:                                               ; preds = %8
  br label %26

16:                                               ; preds = %8
  %17 = icmp slt i32 %13, %2
  br i1 %17, label %18, label %20

18:                                               ; preds = %16
  %19 = add nsw i32 %10, 1
  br label %22

20:                                               ; preds = %16
  %21 = add nsw i32 %10, -1
  br label %22

22:                                               ; preds = %20, %18
  %23 = phi i32 [ %21, %20 ], [ %6, %18 ]
  %24 = phi i32 [ %7, %20 ], [ %19, %18 ]
  br label %5, !llvm.loop !6

25:                                               ; preds = %5
  br label %26

26:                                               ; preds = %25, %15
  %27 = phi i32 [ -1, %25 ], [ %10, %15 ]
  ret i32 %27
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca [5 x i32], align 16
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 16 dereferenceable(20) %1, ptr noundef nonnull align 16 dereferenceable(20) @__const.main.v, i64 20, i1 false)
  %2 = call i32 @buscaBinaria(ptr noundef nonnull %1, i32 noundef 5, i32 noundef 7)
  %3 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %2) #3
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
