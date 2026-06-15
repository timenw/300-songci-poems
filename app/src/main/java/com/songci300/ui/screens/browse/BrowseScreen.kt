package com.songci300.ui.screens.browse

import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.songci300.data.model.Poem
import com.songci300.ui.components.PoemCard
import com.songci300.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BrowseScreen(
    poems: List<Poem>,
    authors: List<String>,
    dynasties: List<String>,
    favoriteIds: Set<Int>,
    onPoemClick: (Int) -> Unit,
    onFavoriteClick: (Int) -> Unit,
    onFilterByCategory: (String) -> Unit,
    onFilterByAuthor: (String) -> Unit,
    onFilterByDynasty: (String) -> Unit,
    onFilterByDifficulty: (Int) -> Unit,
    onBack: () -> Unit,
) {
    var selectedTab by remember { mutableIntStateOf(0) }
    var filterState by remember { mutableStateOf<FilterState?>(null) }
    val tabs = listOf("Theme", "Poet", "Dynasty", "Level")

    // When a filter is applied, show results
    if (filterState != null) {
        FilterResultsView(
            filterState = filterState!!,
            poems = poems,
            favoriteIds = favoriteIds,
            onPoemClick = onPoemClick,
            onFavoriteClick = onFavoriteClick,
            onClearFilter = { filterState = null }
        )
        return
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Browse") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            TabRow(selectedTabIndex = selectedTab) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTab == index,
                        onClick = { selectedTab = index },
                        text = { Text(title) }
                    )
                }
            }

            when (selectedTab) {
                0 -> ThemeFilterContent(
                    onFilter = { theme ->
                        onFilterByCategory(theme)
                        filterState = FilterState.Category(theme)
                    }
                )
                1 -> PoetFilterContent(
                    authors = authors,
                    poems = poems,
                    onFilter = { author ->
                        onFilterByAuthor(author)
                        filterState = FilterState.Author(author)
                    }
                )
                2 -> DynastyFilterContent(
                    dynasties = dynasties,
                    poems = poems,
                    onFilter = { dynasty ->
                        onFilterByDynasty(dynasty)
                        filterState = FilterState.Dynasty(dynasty)
                    }
                )
                3 -> DifficultyFilterContent(
                    poems = poems,
                    onFilter = { level ->
                        onFilterByDifficulty(level)
                        filterState = FilterState.Difficulty(level)
                    }
                )
            }
        }
    }
}

// Filter state sealed class
sealed class FilterState {
    data class Category(val theme: String) : FilterState()
    data class Author(val author: String) : FilterState()
    data class Dynasty(val dynasty: String) : FilterState()
    data class Difficulty(val level: Int) : FilterState()
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun FilterResultsView(
    filterState: FilterState,
    poems: List<Poem>,
    favoriteIds: Set<Int>,
    onPoemClick: (Int) -> Unit,
    onFavoriteClick: (Int) -> Unit,
    onClearFilter: () -> Unit,
) {
    val filteredPoems = when (filterState) {
        is FilterState.Category -> poems.filter { it.category.contains(filterState.theme, ignoreCase = true) }
        is FilterState.Author -> poems.filter { it.author == filterState.author }
        is FilterState.Dynasty -> poems.filter { it.dynastyEn == filterState.dynasty }
        is FilterState.Difficulty -> poems.filter { it.difficulty == filterState.level }
    }

    val title = when (filterState) {
        is FilterState.Category -> "Theme: ${filterState.theme}"
        is FilterState.Author -> filterState.author
        is FilterState.Dynasty -> "${filterState.dynasty}代"
        is FilterState.Difficulty -> "Level ${filterState.level}"
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("$title (${filteredPoems.size})") },
                navigationIcon = {
                    IconButton(onClick = onClearFilter) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        if (filteredPoems.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(
                        Icons.Filled.SearchOff,
                        contentDescription = null,
                        modifier = Modifier.size(64.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        "No poems found",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    TextButton(onClick = onClearFilter) {
                        Text("Choose another")
                    }
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(filteredPoems, key = { it.id ?: 0 }) { poem ->
                    PoemCard(
                        poem = poem,
                        isFavorite = favoriteIds.contains(poem.id),
                        onClick = { poem.id?.let { onPoemClick(it) } },
                        onFavoriteClick = { poem.id?.let { onFavoriteClick(it) } }
                    )
                }
            }
        }
    }
}

@Composable
private fun ThemeFilterContent(
    onFilter: (String) -> Unit
) {
    val themes = listOf(
        "春天" to "\uD83C\uDF38", "花" to "\uD83C\uDF3F", "月亮" to "\uD83C\uDF19", "山水" to "\u26F0\uFE0F",
        "雨" to "\uD83C\uDF27", "风" to "\uD83C\uDF2C", "秋天" to "\uD83C\uDF42", "雪" to "\u2744\uFE0F",
        "夜晚" to "\uD83C\uDF19", "离别" to "\uD83D\uDC4B", "思念" to "\uD83D\uDC95", "孤独" to "\uD83D\uDC64",
        "宴饮" to "\uD83C\uDF77", "祝寿" to "\uD83C\uDF82", "柳" to "\uD83C\uDF32", "婉约" to "\uD83D\uDC96",
    )

    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            Text(
                text = "选择主题",
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.padding(bottom = 8.dp)
            )
        }
        items(themes.chunked(2)) { row ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                row.forEach { (theme, emoji) ->
                    Card(
                        onClick = { onFilter(theme) },
                        modifier = Modifier
                            .weight(1f)
                            .height(72.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f)
                        )
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(12.dp),
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text(text = emoji, style = MaterialTheme.typography.titleMedium)
                            Text(
                                text = theme,
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                }
                if (row.size == 1) Spacer(modifier = Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun PoetFilterContent(
    authors: List<String>,
    poems: List<Poem>,
    onFilter: (String) -> Unit
) {
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        item {
            Text(
                text = "词人",
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.padding(bottom = 8.dp)
            )
        }
        items(authors) { author ->
            val count = poems.count { it.author == author }
            ListItem(
                headlineContent = { Text(author) },
                supportingContent = { Text("$count poems") },
                leadingContent = {
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = MaterialTheme.colorScheme.primaryContainer,
                        modifier = Modifier.size(40.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Text(
                                text = author.first().toString(),
                                style = MaterialTheme.typography.titleMedium,
                                color = MaterialTheme.colorScheme.onPrimaryContainer
                            )
                        }
                    }
                },
                trailingContent = {
                    Icon(Icons.Filled.ChevronRight, contentDescription = null)
                },
                modifier = Modifier.clickable(
                    indication = null,
                    interactionSource = remember { MutableInteractionSource() }
                ) { onFilter(author) }
            )
        }
    }
}

@Composable
private fun DynastyFilterContent(
    dynasties: List<String>,
    poems: List<Poem>,
    onFilter: (String) -> Unit
) {
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        items(dynasties) { dynasty ->
            val count = poems.count { it.dynastyEn == dynasty }
            ListItem(
                headlineContent = { Text("${dynasty}代") },
                supportingContent = { Text("$count poems") },
                trailingContent = {
                    Icon(Icons.Filled.ChevronRight, contentDescription = null)
                },
                modifier = Modifier.clickable(
                    indication = null,
                    interactionSource = remember { MutableInteractionSource() }
                ) { onFilter(dynasty) }
            )
        }
    }
}

@Composable
private fun DifficultyFilterContent(
    poems: List<Poem>,
    onFilter: (Int) -> Unit
) {
    val levels = listOf(
        Triple(1, "Beginner", "Perfect for starting your journey"),
        Triple(2, "Intermediate", "Ready for deeper reading"),
        Triple(3, "Advanced", "For the dedicated reader"),
    )

    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(levels) { (level, title, desc) ->
            val count = poems.count { it.difficulty == level }
            Card(
                onClick = { onFilter(level) },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = when (level) {
                            1 -> SageGreen
                            2 -> DustyBlue
                            else -> Terracotta
                        },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Text(
                                text = level.toString(),
                                style = MaterialTheme.typography.titleLarge,
                                color = WarmWhite
                            )
                        }
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(text = title, style = MaterialTheme.typography.titleMedium)
                        Text(
                            text = desc,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Text(
                        text = "$count",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
