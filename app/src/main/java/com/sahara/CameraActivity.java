package com.sahara;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.media.AudioManager;
import android.media.Image;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.util.Rational;
import android.util.Size;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Locale;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraX;
import androidx.camera.core.FlashMode;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureConfig;
import androidx.camera.core.ImageProxy;
import androidx.camera.core.Preview;
import androidx.camera.core.PreviewConfig;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;


public class CameraActivity extends AppCompatActivity {


    private int REQUEST_CODE_PERMISSIONS = 101;
    private final String[] REQUIRED_PERMISSIONS = new String[]{"android.permission.CAMERA", "android.permission.RECORD_AUDIO"};
    public TextureView textureView;
    public static String SERVER_IP;
    public static int SERVER_PORT;
    public static Communicate connObj;
    public static Communicate.SendData sendDataThread;
    public ImageCapture imgCap;
    public static TextToSpeech tts;
    public static String ttsStatus;
    public SpeechRecognizer speechRecognizer;
    public Intent speechRecognizerIntent;
    public String speechText;
    public ConstraintLayout mainLayout;
    public Boolean capturing;
    public byte [] imgBytes;
    public int clickType;

    public CameraActivity()
    {
        capturing = false;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
        SharedPreferences prefs = getSharedPreferences("prefs", MODE_PRIVATE);
        boolean firstStart = prefs.getBoolean("firstStart", true);

        if (firstStart) {
            showStartDialog();
        }
        getSupportActionBar().hide();

        mainLayout = findViewById(R.id.cameraFullScreen);

        textureView = findViewById(R.id.view_finder);
        int size  = 500; //Resources.getSystem().getDisplayMetrics().widthPixels;
        textureView.getLayoutParams().width = size;
        textureView.getLayoutParams().height = size;

        if(allPermissionsGranted()){
            startCamera(); //start camera if permission has been granted by user
        } else{
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS);
        }

        SERVER_IP = "192.168.100.7";
        SERVER_PORT = 7100;

        connObj = new Communicate(SERVER_IP, SERVER_PORT);


        /* Initializing the TTS engine and hooking a listener to it. */

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR){
                    int result = tts.setLanguage(Locale.ENGLISH);
                    if (result  == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED){

                        ttsStatus = "LANG_UNSUPPORTED";
                    }
                    else{
                        ttsStatus = "SUCCESS";
                        tts.setSpeechRate((float)1.5);
                    }
                }

            }
        });

        setVolumeControlStream(AudioManager.STREAM_MUSIC);

        /* Initializing the STT engine and hooking a listener to it. */

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        speechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());


        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle params) {}
            @Override
            public void onBeginningOfSpeech() {}
            @Override
            public void onRmsChanged(float rmsdB) {}
            @Override
            public void onBufferReceived(byte[] buffer) {}
            @Override
            public void onEndOfSpeech() {}
            @Override
            public void onError(int error) {}
            @Override
            public void onResults(Bundle bundle) {
                //Getting all the matches
                ArrayList<String> matches = bundle.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);

                //Storing the first most confident match
                if (matches != null) {
                    speechText = matches.get(0);

                    if(clickType==1)
                    {
                        /* Send the captured image along with the command on user tap. */
                        ByteArrayOutputStream data = new ByteArrayOutputStream();
                        try {

                            data.write(imgBytes);
                            data.write("mof".getBytes());
                            data.write(speechText.getBytes());

                            byte[] out = data.toByteArray();

                            sendDataThread = new Communicate.SendData(out);
                            sendDataThread.start();

                            //String msg = Communicate.message;//connObj.getMessage();


                        } catch (IOException e) {
                            e.printStackTrace();
                        }

                    }

                }
            }
            @Override
            public void onPartialResults(Bundle bundle) {}
            @Override
            public void onEvent(int i, Bundle bundle) {}

        });

    }
    private void showStartDialog() {
        new AlertDialog.Builder(this)
                .setTitle("Disclaimer")
                .setMessage("Welcome to Divya Drishti.You utilize the app using various voice commands.The voice commands specific for the task to be done are,Currency or Cash for Currency Detection,Total Cash for Currency Totaling,Mask for Whether a person is wearing a mask,Object for Detecting everyday life objects,Read Text for Reading all text available,Summary for reading and summarizing text,Bill for extracting total amount from a bill,Colour for Detecting colour around.")
                .setPositiveButton("ACCEPT", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String text4 = "Welcome to our App Divya Drishti. You utilize the app using various voice commands.The voice commands specific for the task to be done are,Currency or Cash for Currency Detection,Total Cash for Currency Totaling,Mask for Whether a person is wearing a mask,Object for Detecting everyday life objects,Read Text for Reading all text available,Summary for reading and summarizing text,Bill for extracting total amount from a bill,Colour for Detecting colour around.";
                        String text3 = "Welcome to our App Divya Drishti.\n"+ " You utilize the app using various voice commands.\n" + "The voice commands specific for the task to be done are.\n" + "Currency or Cash for Currency Detection.\n" + "Total Cash for Currency Totaling.\n" + "Mask for Whether a person is wearing a mask.\n" + "Object for Detecting everyday life objects.\n" + "Read Text for Reading all text available.\n" + "Summary for reading and summarizing text.\n" + "Bill for extracting total amount from a bill.\n" + "Colour for Detecting colour around.";
                        tts.speak(text3, TextToSpeech.QUEUE_ADD, null, null);
                        dialog.dismiss();
                    }
                })
                .create().show();
        SharedPreferences prefs = getSharedPreferences("prefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();
        editor.putBoolean("firstStart", false);
        editor.apply();
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    private void screenTapListener(Boolean singleClick)
    {

        if(singleClick)
        {
            clickType = 1;
            /* User taps to capture the image and simultaneously start the recording. */
            if (!capturing)
            {
                /* Start capturing */
                capturing = true;

                if(connObj.connectionStatus.equals("SUCCESS"))
                {
                    /* Capture image */
                    imgCap.takePicture(new ImageCapture.OnImageCapturedListener() {
                        @Override
                        public void onCaptureSuccess(ImageProxy imageProxy, int rotationDegrees) {
                            super.onCaptureSuccess(imageProxy, rotationDegrees);

                            //Image image = imageProxy.getImage();

                            Bitmap bitmap = textureView.getBitmap();
                            //bitmap = Bitmap.createScaledBitmap(bitmap, 500, 500, true);

                            ByteArrayOutputStream baos=new ByteArrayOutputStream();
                            bitmap.compress(Bitmap.CompressFormat.PNG,100, baos);
                            imgBytes = baos.toByteArray();

                        }
                    });

                    /* Start listening to the voice command. */
                    speechRecognizer.startListening(speechRecognizerIntent);
                }
                else
                {
                    speakText("You are not connected to the server. Please reconnect to the server.");
                    capturing = false;
                }
            }
            else
            {
                /* Stop capturing */
                capturing = false;

                /* Stop listening to the voice command and send the captured image along with the voice command to the server */
                speechRecognizer.stopListening();
            }
        }
        else
        {
            clickType=2;
            capturing = false;
            /* User double taps to capture the image again. Previous recording of the voice command needs to be ignored. */
            speechRecognizer.stopListening();
        }
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    private boolean allPermissionsGranted(){
        for(String permission : REQUIRED_PERMISSIONS){
            if(ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED){
                return false;
            }
        }
        return true;
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    private void startCamera() {

        CameraX.unbindAll();

        Size screen = new Size(textureView.getWidth(), textureView.getHeight()); //size of the screen


        PreviewConfig pConfig = new PreviewConfig.Builder()
                .setTargetAspectRatio(new Rational(1, 1))
                .setTargetResolution(screen)
                .build();
        Preview preview = new Preview(pConfig);


        preview.setOnPreviewOutputUpdateListener(
                new Preview.OnPreviewOutputUpdateListener() {
                    @Override
                    public void onUpdated(Preview.PreviewOutput output){
                        ViewGroup parent = (ViewGroup) textureView.getParent();
                        parent.removeView(textureView);
                        parent.addView(textureView, 0);

                        textureView.setSurfaceTexture(output.getSurfaceTexture());
                        updateTransform();
                    }
                });


        ImageCaptureConfig imageCaptureConfig = new ImageCaptureConfig.Builder()
                .setCaptureMode(ImageCapture.CaptureMode.MAX_QUALITY)
                .setFlashMode(FlashMode.AUTO)
                .setTargetRotation(getWindowManager()
                .getDefaultDisplay()
                .getRotation()).build();

        imgCap = new ImageCapture(imageCaptureConfig);

        mainLayout.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                screenTapListener(false);
            }

            @Override
            public void onSingleClick() {
                screenTapListener(true);
            }
        });

        //bind to lifecycle:
        CameraX.bindToLifecycle(this, imgCap, preview);
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    private void updateTransform(){
        Matrix mx = new Matrix();
        float w = textureView.getMeasuredWidth();
        float h = textureView.getMeasuredHeight();

        float cX = w / 2f;
        float cY = h / 2f;

        int rotationDgr;
        int rotation = (int)textureView.getRotation();

        switch(rotation){
            case Surface.ROTATION_0:
                rotationDgr = 0;
                break;
            case Surface.ROTATION_90:
                rotationDgr = 90;
                break;
            case Surface.ROTATION_180:
                rotationDgr = 180;
                break;
            case Surface.ROTATION_270:
                rotationDgr = 270;
                break;
            default:
                return;
        }

        mx.postRotate((float)rotationDgr, cX, cY);
        textureView.setTransform(mx);
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {

        if(requestCode == REQUEST_CODE_PERMISSIONS)
        {
            if(allPermissionsGranted())
            {
                startCamera();
            }
            else
            {
                Toast.makeText(this, "Permissions not granted by the user.", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    public static void speakText(String text)
    {
        while(true)
        {
            if(ttsStatus.equals("SUCCESS"))
            {
                /* For newer android versions. */
                if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP){
                    tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
                }

                /* For older android versions. */
                else {
                    tts.speak(text, TextToSpeech.QUEUE_FLUSH, null);
                }
                break;
            }
        }
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/

    @Override
    public void onPause() {

        /* Disable TTS when your app is not in the foreground */
        if (tts != null) {
            tts.stop();
            tts.shutdown();

        }
        super.onPause();
    }

    @Override
    public void onResume()
    {

        /* Disable TTS when your app is not in the foreground */

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR){
                    int result = tts.setLanguage(Locale.ENGLISH);
                    if (result  == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED){

                        ttsStatus = "LANG_UNSUPPORTED";
                    }
                    else{
                        ttsStatus = "SUCCESS";
                        tts.setSpeechRate((float)1.5);
                    }
                }

            }
        });

        super.onResume();
    }

    @Override
    public void onDestroy() {

        /* Disable TTS when your app is not in the foreground */
        if (tts != null) {
            tts.stop();
            tts.shutdown();

        }
        super.onDestroy();
    }

    /*-------------------------------------------------------------------------------------------------------------------------*/
}

abstract class DoubleClickListener implements View.OnClickListener {
    private static final long DEFAULT_QUALIFICATION_SPAN = 200;
    private boolean isSingleEvent;
    private long doubleClickQualificationSpanInMillis;
    private long timestampLastClick;
    private Handler handler;
    private Runnable runnable;

    public DoubleClickListener() {
        doubleClickQualificationSpanInMillis = DEFAULT_QUALIFICATION_SPAN;
        timestampLastClick = 0;
        handler = new Handler();
        runnable = new Runnable() {
            @Override
            public void run() {
                if (isSingleEvent) {
                    onSingleClick();
                }
            }
        };
    }

    @Override
    public void onClick(View v) {
        if((SystemClock.elapsedRealtime() - timestampLastClick) < doubleClickQualificationSpanInMillis) {
            isSingleEvent = false;
            handler.removeCallbacks(runnable);
            onDoubleClick();
            return;
        }

        isSingleEvent = true;
        handler.postDelayed(runnable, DEFAULT_QUALIFICATION_SPAN);
        timestampLastClick = SystemClock.elapsedRealtime();
    }

    public abstract void onDoubleClick();
    public abstract void onSingleClick();
}