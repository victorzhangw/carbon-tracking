package com.aicares.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.webkit.*
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var progressBar: ProgressBar
    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    
    // 後端伺服器網址
    // 本地開發環境
    private val SERVER_URL = "http://192.168.1.102:5000/"
    
    // 生產環境（部署後使用）
    // private val SERVER_URL = "https://your-domain.com/"
    
    private val PERMISSION_REQUEST_CODE = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // 初始化 UI 元件
        webView = findViewById(R.id.webview)
        progressBar = findViewById(R.id.progressBar)
        swipeRefreshLayout = findViewById(R.id.swipeRefreshLayout)
        
        // 設定 WebView
        setupWebView()
        
        // 設定下拉重新整理
        setupSwipeRefresh()
        
        // 請求權限
        requestPermissions()
        
        // 檢查網路連線
        if (isNetworkAvailable()) {
            loadUrl(SERVER_URL)
        } else {
            showNoInternetDialog()
        }
    }

    private fun requestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.MODIFY_AUDIO_SETTINGS
        )
        
        val permissionsToRequest = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        
        if (permissionsToRequest.isNotEmpty()) {
            ActivityCompat.requestPermissions(
                this,
                permissionsToRequest.toTypedArray(),
                PERMISSION_REQUEST_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            val deniedPermissions = permissions.filterIndexed { index, _ ->
                grantResults[index] != PackageManager.PERMISSION_GRANTED
            }
            
            if (deniedPermissions.isNotEmpty()) {
                Toast.makeText(
                    this,
                    "部分功能需要權限才能使用（如語音錄製）",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val webSettings: WebSettings = webView.settings
        
        // 啟用 JavaScript
        webSettings.javaScriptEnabled = true
        
        // 啟用 DOM Storage
        webSettings.domStorageEnabled = true
        
        // 啟用資料庫
        webSettings.databaseEnabled = true
        
        // 快取設定
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT
        
        // 檔案存取
        webSettings.allowFileAccess = true
        webSettings.allowContentAccess = true
        
        // 支援縮放
        webSettings.setSupportZoom(true)
        webSettings.builtInZoomControls = true
        webSettings.displayZoomControls = false
        
        // 自適應螢幕
        webSettings.useWideViewPort = true
        webSettings.loadWithOverviewMode = true
        
        // 混合內容模式
        webSettings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        
        // 啟用媒體播放
        webSettings.mediaPlaybackRequiresUserGesture = false
        
        // 設定 User Agent
        webSettings.userAgentString = webSettings.userAgentString + " AICares/1.0"
        
        // WebViewClient
        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                super.onPageStarted(view, url, favicon)
                progressBar.visibility = View.VISIBLE
            }
            
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                progressBar.visibility = View.GONE
                swipeRefreshLayout.isRefreshing = false
            }
            
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame == true) {
                    showErrorPage()
                }
            }
            
            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                // 允許所有內部連結
                return false
            }
        }
        
        // WebChromeClient
        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                super.onProgressChanged(view, newProgress)
                progressBar.progress = newProgress
            }
            
            override fun onPermissionRequest(request: PermissionRequest?) {
                // 自動授予 WebView 的媒體權限請求
                request?.grant(request.resources)
            }
            
            override fun onJsAlert(
                view: WebView?,
                url: String?,
                message: String?,
                result: JsResult?
            ): Boolean {
                AlertDialog.Builder(this@MainActivity)
                    .setTitle("提示")
                    .setMessage(message)
                    .setPositiveButton("確定") { _, _ -> result?.confirm() }
                    .setCancelable(false)
                    .create()
                    .show()
                return true
            }
            
            override fun onJsConfirm(
                view: WebView?,
                url: String?,
                message: String?,
                result: JsResult?
            ): Boolean {
                AlertDialog.Builder(this@MainActivity)
                    .setTitle("確認")
                    .setMessage(message)
                    .setPositiveButton("確定") { _, _ -> result?.confirm() }
                    .setNegativeButton("取消") { _, _ -> result?.cancel() }
                    .setCancelable(false)
                    .create()
                    .show()
                return true
            }
        }
        
        // 啟用除錯模式
        WebView.setWebContentsDebuggingEnabled(true)
    }
    
    private fun setupSwipeRefresh() {
        swipeRefreshLayout.setColorSchemeResources(
            R.color.primary,
            R.color.primary_dark,
            R.color.accent
        )
        
        swipeRefreshLayout.setOnRefreshListener {
            webView.reload()
        }
    }
    
    private fun loadUrl(url: String) {
        webView.loadUrl(url)
    }
    
    private fun isNetworkAvailable(): Boolean {
        val connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        
        return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
               capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
               capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
    }
    
    private fun showNoInternetDialog() {
        AlertDialog.Builder(this)
            .setTitle("無網路連線")
            .setMessage("請檢查網路連線後重試")
            .setPositiveButton("重試") { _, _ ->
                if (isNetworkAvailable()) {
                    loadUrl(SERVER_URL)
                } else {
                    showNoInternetDialog()
                }
            }
            .setNegativeButton("離開") { _, _ -> finish() }
            .setCancelable(false)
            .create()
            .show()
    }
    
    private fun showErrorPage() {
        val errorHtml = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: 'Microsoft JhengHei', Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        text-align: center;
                        padding: 20px;
                    }
                    .error-container {
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        max-width: 400px;
                    }
                    h1 {
                        color: #667eea;
                        font-size: 3em;
                        margin: 0;
                    }
                    h2 {
                        color: #333;
                        margin: 10px 0;
                    }
                    p {
                        color: #666;
                        font-size: 1.1em;
                        margin: 20px 0;
                    }
                    ul {
                        text-align: left;
                        color: #666;
                    }
                    button {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        padding: 12px 30px;
                        border-radius: 25px;
                        font-size: 1em;
                        cursor: pointer;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>😕</h1>
                    <h2>無法連線</h2>
                    <p>無法連接到伺服器，請檢查：</p>
                    <ul>
                        <li>網路連線是否正常</li>
                        <li>伺服器是否運行中</li>
                        <li>伺服器地址：<br><small>$SERVER_URL</small></li>
                    </ul>
                    <button onclick="location.reload()">重新載入</button>
                </div>
            </body>
            </html>
        """.trimIndent()
        
        webView.loadDataWithBaseURL(null, errorHtml, "text/html", "UTF-8", null)
    }
    
    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }
    
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        webView.saveState(outState)
    }
    
    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        super.onRestoreInstanceState(savedInstanceState)
        webView.restoreState(savedInstanceState)
    }
    
    override fun onPause() {
        super.onPause()
        webView.onPause()
        webView.pauseTimers()
    }
    
    override fun onResume() {
        super.onResume()
        webView.onResume()
        webView.resumeTimers()
    }
    
    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
