import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import com.jfoenix.controls.*;
public class Controller extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage){
        try{
            Parent root = FXMLLoader.load(getClass().getResource("client.fxml"));

            Scene scene = new Scene(root, 900, 600);

            stage.setTitle("Simple User Database");
            stage.setScene(scene);
            stage.show();
        }catch(Exception e){
            e.printStackTrace();
            System.out.println("ERROR");
        }

    }
}
