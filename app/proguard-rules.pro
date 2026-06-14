# ProGuard rules for SongCi300
-keep class com.songci300.data.model.** { *; }
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.**
-keep class com.android.billingclient.api.** { *; }
