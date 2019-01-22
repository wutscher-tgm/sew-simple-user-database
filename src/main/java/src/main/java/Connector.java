package main.java;

import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;

import java.io.IOException;

public class Connector {
    private OkHttpClient client = new OkHttpClient();
    private String url;
    public Connector(String url){
        this.url = url;
    }

    public String get() throws IOException {
        Request request = new Request.Builder()
                .url("http://localhost:5000/students")
                .build();
        return client.newCall(request).execute().body().string();
    }

    public void update(String email, String username) throws IOException {
        String postBody = "";

        final MediaType MEDIA_TYPE_MARKDOWN
                = MediaType.parse("text/x-markdown; charset=utf-8");

        Request request = new Request.Builder()
                .url(this.url+"/students?email="+email+"&username="+username)
                .patch(RequestBody.create(MEDIA_TYPE_MARKDOWN, postBody))
                .build();

        this.client.newCall(request).execute().body().string();
    }

    public void delete(String email) throws IOException {
        String postBody = "";

        final MediaType MEDIA_TYPE_MARKDOWN
                = MediaType.parse("text/x-markdown; charset=utf-8");

        Request request = new Request.Builder()
                .url(this.url+"/students?email="+email)
                .delete(RequestBody.create(MEDIA_TYPE_MARKDOWN, postBody))
                .build();

        this.client.newCall(request).execute().body().string();
    }


    public void create(String email, String username, String pictureLink) throws IOException {
        String postBody = "";

        final MediaType MEDIA_TYPE_MARKDOWN
                = MediaType.parse("text/x-markdown; charset=utf-8");

        String path = this.url+"/students?email="+email+"&username="+username;

        if(!pictureLink.equals("")){
            path += "&pictureLink="+pictureLink;
        }
        Request request = new Request.Builder()
                .url(path)
                .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, postBody))
                .build();

        this.client.newCall(request).execute().body().string();
    }


}
