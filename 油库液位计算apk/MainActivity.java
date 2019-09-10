package com.example.administrator.oil_2;


import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    private EditText et_frist;
    private EditText et_second;
    private EditText et_result;
    private EditText et_result1;
    private EditText et_result2;
    private EditText et_result3;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        et_frist = findViewById(R.id.et_frist);
        et_second = findViewById(R.id.et_second);
        et_result = findViewById(R.id.et_result);
        et_result1 = findViewById(R.id.et_result1);
        et_result2 = findViewById(R.id.et_result2);
        et_result3 = findViewById(R.id.et_result3);

    }

    public void doCount(View view){
        double oil_R = 1.2;
        double oil_L = 6.05;
        double oil_C = 0.6;
        String str1= et_frist.getText().toString();
        String str2 = et_second.getText().toString();
        // 转换成int

        double oil_H1 = Double.valueOf(str1.toString());
        double oil_H2 = Double.valueOf(str2.toString());
        double num3 = (oil_L*((Math.PI * Math.pow(oil_R, 2))/2-(oil_R-oil_H1)*Math.sqrt(2*oil_H1*oil_R-Math.pow(oil_H1, 2))-Math.pow(oil_R, 2)*Math.asin(1-oil_H1/oil_R))+(Math.PI*oil_C)/(3*oil_R)*(3*Math.pow(oil_R, 2)*oil_H1-Math.pow(oil_R, 3)+Math.pow(oil_R-oil_H1, 3)))*1000;
        double num4 = (oil_L*((Math.PI * Math.pow(oil_R, 2))/2-(oil_R-oil_H2)*Math.sqrt(2*oil_H2*oil_R-Math.pow(oil_H2, 2))-Math.pow(oil_R, 2)*Math.asin(1-oil_H2/oil_R))+(Math.PI*oil_C)/(3*oil_R)*(3*Math.pow(oil_R, 2)*oil_H2-Math.pow(oil_R, 3)+Math.pow(oil_R-oil_H2, 3)))*1000;
        double num5 = (num3+num4);
        double num6 = (num3+num4)-7000;
        //转换成String
        et_result.setText(num3+"");
        et_result1.setText(num4+"");
        et_result2.setText(num5+"");
        et_result3.setText(num6+"");

    }
    public void doClear(View view){
        et_frist.setText("");
        et_second.setText("");
        et_result.setText("");
        et_result1.setText("");
        et_result2.setText("");
        et_result3.setText("");
        et_frist.requestFocus();

    }
    public void doExit(View view){
        finish();
    }
}
