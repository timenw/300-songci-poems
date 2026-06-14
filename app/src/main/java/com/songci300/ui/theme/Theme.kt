package com.songci300.ui.theme

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

// Warm, literary color palette for Western audiences
val WarmWhite = Color(0xFFFAF8F5)
val SoftCream = Color(0xFFF5F0E8)
val InkBlack = Color(0xFF2C2C2C)
val WarmGray = Color(0xFF6B6560)
val DustyBlue = Color(0xFF5B7B8A)
val Terracotta = Color(0xFFC4704B)
val SageGreen = Color(0xFF7A8B6F)
val DeepIndigo = Color(0xFF3D4F6F)
val MutedGold = Color(0xFFC9A96E)
val SoftBlush = Color(0xFFE8D5C4)

private val PoemColorScheme = lightColorScheme(
    primary = DeepIndigo,
    onPrimary = WarmWhite,
    primaryContainer = SoftCream,
    onPrimaryContainer = InkBlack,
    secondary = DustyBlue,
    onSecondary = WarmWhite,
    secondaryContainer = Color(0xFFD4E4EC),
    onSecondaryContainer = InkBlack,
    tertiary = Terracotta,
    onTertiary = WarmWhite,
    tertiaryContainer = SoftBlush,
    onTertiaryContainer = InkBlack,
    background = WarmWhite,
    onBackground = InkBlack,
    surface = WarmWhite,
    onSurface = InkBlack,
    surfaceVariant = SoftCream,
    onSurfaceVariant = WarmGray,
    outline = Color(0xFFD0C8BC),
    outlineVariant = Color(0xFFE8E0D4),
)

@Composable
fun SongCi300Theme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = PoemColorScheme,
        typography = PoemTypography,
        content = content
    )
}

val PoemTypography = Typography(
    displayLarge = Typography().displayLarge.copy(
        color = InkBlack,
        fontWeight = FontWeight.Light
    ),
    headlineLarge = Typography().headlineLarge.copy(
        color = InkBlack,
        fontWeight = FontWeight.Normal
    ),
    headlineMedium = Typography().headlineMedium.copy(
        color = InkBlack,
        fontWeight = FontWeight.Normal
    ),
    titleLarge = Typography().titleLarge.copy(
        color = InkBlack,
        fontWeight = FontWeight.Medium
    ),
    titleMedium = Typography().titleMedium.copy(
        color = InkBlack,
        fontWeight = FontWeight.Medium
    ),
    bodyLarge = Typography().bodyLarge.copy(
        color = InkBlack,
        lineHeight = 28.sp
    ),
    bodyMedium = Typography().bodyMedium.copy(
        color = WarmGray,
        lineHeight = 24.sp
    ),
    labelLarge = Typography().labelLarge.copy(
        color = WarmGray,
        fontWeight = FontWeight.Medium
    ),
)
