import java.nio.file.Paths
import resource._
import scala.io.Source._
import scala.collection.mutable.ArrayBuffer
// Needed for Scoring
import ml.combust.mleap.runtime.MleapSupport._
import ml.combust.mleap.runtime.serialization.FrameReader
import ml.combust.mleap.runtime.frame.Transformer
import ml.combust.bundle.BundleFile

object AirbnbScoring {
    var mleapTransformerLr: Transformer = null;
    var mleapTransformerRf: Transformer = null;
    var schemaStr: String = null;

    def init() = {
        val cwd = Paths.get("").toAbsolutePath().toUri().toString()
        // Deserialize models from bundle.ml 
        mleapTransformerLr = (for(bf <- managed(BundleFile("jar:" + cwd + "model/airbnb.model.lr.zip"))) yield {
                                        bf.loadMleapBundle().get.root
                                    }).tried.get    
        mleapTransformerRf = (for(bf <- managed(BundleFile("jar:" + cwd + "model/airbnb.model.rf.zip"))) yield {
                                        bf.loadMleapBundle().get.root
                                    }).tried.get
        // Read in schema for input
        val source = scala.io.Source.fromFile("model/schema.json")
        schemaStr = try source.mkString finally source.close()
    }

    def score(rows : String): Array[Array[Double]] = {
        var bytes = s"""{"schema": $schemaStr, "rows": $rows}""".getBytes("UTF-8")
        var predictions = new ArrayBuffer[Array[Double]]()

        // Deserialize and score a leapFrame from json
        for(frame <- FrameReader("ml.combust.mleap.json").fromBytes(bytes);
            frameLr <- mleapTransformerLr.transform(frame);
            frameLrSelect <- frameLr.select("price_prediction");
            frameRf <- mleapTransformerRf.transform(frame);
            frameRfSelect <- frameRf.select("price_prediction");
            row_num <- 0 to frame.dataset.toSeq.size-1) {
                predictions += Array(
                    frameLrSelect.dataset(row_num).getDouble(0),  // Prediction using linear regression model
                    frameRfSelect.dataset(row_num).getDouble(0)); // Prediction using random forest model
            }

        return predictions.toArray
    }
}