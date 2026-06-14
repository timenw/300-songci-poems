package com.poem300

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log

class SplashActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("Splash", "onCreate")
        startActivity(Intent(this, MainActivity::class.java))
        finish()
    }
}
