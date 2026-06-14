package com.poem300

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log

class SplashActivity : Activity() {

    companion object {
        private const val TAG = "Splash"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "onCreate")

        // 延迟 1.5 秒后跳转
        Handler(Looper.getMainLooper()).postDelayed({
            try {
                startActivity(Intent(this, MainActivity::class.java))
                finish()
            } catch (e: Exception) {
                Log.e(TAG, "Failed to start MainActivity: ${e.message}")
            }
        }, 1500)
    }
}
