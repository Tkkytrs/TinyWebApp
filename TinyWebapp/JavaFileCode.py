data = """package com.theprojectdamper.theexecutableeebview.appforpy;

import android.Manifest;
import android.app.Activity;
import android.graphics.Bitmap;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends Activity {

	private WebView webview1;
	private Timer _timer = new Timer();
	private TimerTask x;

	private String prevUrl = "", prevCd = "", ccc = "";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		webview1 = findViewById(R.id.webview1);
		webview1.getSettings().setJavaScriptEnabled(true);
		webview1.getSettings().setDomStorageEnabled(true);
		webview1.getSettings().setSupportZoom(true);
		webview1.getSettings().setCacheMode(WebSettings.LOAD_NO_CACHE);
		webview1.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
		webview1.setWebChromeClient(new WebChromeClient());

		webview1.setWebViewClient(new WebViewClient() {
			@Override
			public void onPageStarted(WebView view, String url, Bitmap favicon) {
				writeFile("current.txt", url);
				super.onPageStarted(view, url, favicon);
			}
		});

		initializeLogic();
	}

	private void initializeLogic() {
		transparentStatusBar();

		// Ensure necessary files exist
		createFileIfNotExists("url.txt", "https://google.com");
		createFileIfNotExists("current.txt", "https://google.com");
		createFileIfNotExists("cd.txt", "https://google.com");
		createFileIfNotExists("cdo.txt", "https://google.com");

		// Load initial URL
		prevUrl = readFile("url.txt");
		webview1.loadUrl(prevUrl);

		// Timer for auto-handling
		x = new TimerTask() {
			@Override
			public void run() {
				runOnUiThread(() -> {
					String currentUrl = readFile("url.txt");
					if (!prevUrl.equals(currentUrl)) {
						prevUrl = currentUrl;
						webview1.loadUrl(currentUrl);
					}

					// Save progress
					writeFile("prog.txt", String.valueOf(webview1.getProgress()));

					// Check for HTML scrape command
					if (fileExists("shcd.txt")) {
						deleteFile("shcd.txt");
						webview1.evaluateJavascript("(function() { return document.documentElement.innerHTML; })();", new ValueCallback<String>() {
							@Override
							public void onReceiveValue(String html) {
								writeFile("htm.txt", html);
							}
						});
					}

					// CD & CDO commands
					String newCd = readFile("cd.txt");
					if (!prevCd.equals(newCd)) {
						prevCd = newCd;
						webview1.loadUrl(prevCd);
						showMessage("js_executed");
					}

					String newCcc = readFile("cdo.txt");
					if (!ccc.equals(newCcc)) {
						ccc = newCcc;
						webview1.loadUrl(ccc);
					}
				});
			}
		};

		_timer.scheduleAtFixedRate(x, 100, 250);
	}

	// -------- Helper Methods --------

	private String getBaseDirectory() {
		String os = System.getProperty("os.name").toLowerCase();
		String path;

		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT && os.contains("linux")) {
			path = "/storage/emulated/0/.weblauncher/";
		} else if (os.contains("windows")) {
			path = System.getenv("USERPROFILE") + File.separator + "weblauncher" + File.separator;
		} else {
			path = System.getProperty("user.home") + File.separator + "weblauncher" + File.separator;
		}

		File dir = new File(path);
		if (!dir.exists()) dir.mkdirs();
		return path;
	}

	private void writeFile(String filename, String content) {
		try {
			FileOutputStream fos = new FileOutputStream(new File(getBaseDirectory(), filename));
			fos.write(content.getBytes());
			fos.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private String readFile(String filename) {
		try {
			File file = new File(getBaseDirectory(), filename);
			if (!file.exists()) return "";
			byte[] data = new byte[(int) file.length()];
			java.io.FileInputStream fis = new java.io.FileInputStream(file);
			fis.read(data);
			fis.close();
			return new String(data);
		} catch (Exception e) {
			e.printStackTrace();
			return "";
		}
	}

	private void createFileIfNotExists(String filename, String defaultContent) {
		File file = new File(getBaseDirectory(), filename);
		if (!file.exists()) {
			writeFile(filename, defaultContent);
		}
	}

	private void deleteFile(String filename) {
		File file = new File(getBaseDirectory(), filename);
		if (file.exists()) file.delete();
	}

	private boolean fileExists(String filename) {
		File file = new File(getBaseDirectory(), filename);
		return file.exists();
	}

	private void showMessage(String msg) {
		Toast.makeText(getApplicationContext(), msg, Toast.LENGTH_SHORT).show();
	}

	private void transparentStatusBar() {
		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
			Window w = this.getWindow();
			w.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
			w.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
			w.setStatusBarColor(0xFF008375);
			w.setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS, WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
		}
	}
}
"""