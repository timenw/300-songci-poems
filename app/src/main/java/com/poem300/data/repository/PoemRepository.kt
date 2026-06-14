package com.songci300.data.repository

import com.songci300.data.db.FavoriteDao
import com.songci300.data.db.PoemDao
import com.songci300.data.model.Favorite
import com.songci300.data.model.Poem
import kotlinx.coroutines.flow.Flow

class PoemRepository(
    private val poemDao: PoemDao,
    private val favoriteDao: FavoriteDao
) {
    fun getAllPoems(): Flow<List<Poem>> = poemDao.getAllPoems()

    suspend fun getPoemById(id: Int): Poem? = poemDao.getPoemById(id)

    fun getPoemsByAuthor(author: String): Flow<List<Poem>> = poemDao.getPoemsByAuthor(author)

    fun getPoemsByCategory(category: String): Flow<List<Poem>> = poemDao.getPoemsByCategory(category)

    fun searchPoems(query: String): Flow<List<Poem>> = poemDao.searchPoems(query)

    fun getAllAuthors(): Flow<List<String>> = poemDao.getAllAuthors()

    fun getAllDynasties(): Flow<List<String>> = poemDao.getAllDynasties()

    fun getPoemsByDifficulty(level: Int): Flow<List<Poem>> = poemDao.getPoemsByDifficulty(level)

    suspend fun getDailyPoem(): Poem? {
        val calendar = java.util.Calendar.getInstance()
        val dayOfYear = calendar.get(java.util.Calendar.DAY_OF_YEAR)
        val count = poemDao.getCount()
        if (count == 0) return null
        val id = (dayOfYear % count) + 1
        return poemDao.getPoemById(id) ?: poemDao.getRandomPoem()
    }

    fun getFavoritePoems(): Flow<List<Poem>> = favoriteDao.getFavoritePoems()

    fun getFavoriteIds(): Flow<List<Int>> = favoriteDao.getFavoriteIds()

    fun isFavorite(poemId: Int): Flow<Boolean> = favoriteDao.isFavorite(poemId)

    suspend fun addFavorite(poemId: Int) {
        favoriteDao.addFavorite(Favorite(poemId = poemId))
    }

    suspend fun removeFavorite(poemId: Int) {
        favoriteDao.removeFavorite(poemId)
    }

    suspend fun updateNote(poemId: Int, note: String) {
        favoriteDao.updateNote(poemId, note)
    }

    suspend fun getFavoriteCount(): Int = favoriteDao.getFavoriteCount()
}
