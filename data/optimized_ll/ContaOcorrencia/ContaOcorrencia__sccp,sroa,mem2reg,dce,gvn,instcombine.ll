; ModuleID = 'data/original_ll/ContaOcorrencia.ll'
source_filename = "data/c_codes/ContaOcorrencia.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@__const.main.v = private unnamed_addr constant [7 x i32] [i32 2, i32 3, i32 2, i32 5, i32 2, i32 3, i32 4], align 16
@.str = private unnamed_addr constant [31 x i8] c"O n\C3\BAmero %d aparece %d vezes\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @contar(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  br label %4

4:                                                ; preds = %13, %3
  %.07 = phi i32 [ 0, %3 ], [ %.1, %13 ]
  %.0 = phi i32 [ 0, %3 ], [ %14, %13 ]
  %5 = icmp slt i32 %.0, %1
  br i1 %5, label %6, label %15

6:                                                ; preds = %4
  %7 = zext nneg i32 %.0 to i64
  %8 = getelementptr inbounds nuw i32, ptr %0, i64 %7
  %9 = load i32, ptr %8, align 4
  %10 = icmp eq i32 %9, %2
  br i1 %10, label %11, label %13

11:                                               ; preds = %6
  %12 = add nsw i32 %.07, 1
  br label %13

13:                                               ; preds = %11, %6
  %.1 = phi i32 [ %12, %11 ], [ %.07, %6 ]
  %14 = add nuw nsw i32 %.0, 1
  br label %4, !llvm.loop !6

15:                                               ; preds = %4
  ret i32 %.07
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca [7 x i32], align 16
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 16 dereferenceable(28) %1, ptr noundef nonnull align 16 dereferenceable(28) @__const.main.v, i64 28, i1 false)
  %2 = call i32 @contar(ptr noundef nonnull %1, i32 noundef 7, i32 noundef 2)
  %3 = call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef 2, i32 noundef %2) #3
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
