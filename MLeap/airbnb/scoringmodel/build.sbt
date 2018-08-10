lazy val root = (project in file(".")).
    settings(
        name := "mleap-airbnb",
        version := "0.0.1",
        scalaVersion := "2.11.5",
        crossScalaVersions := Seq("2.11.5", "2.10.5"),
        mainClass in Compile := Some("AirbnbScoring")        
    )

libraryDependencies ++= Seq(
    "ml.combust.mleap" %% "mleap-runtime" % "0.10.1"
)

assemblyOutputPath in assembly := file("./mleap-airbnb-assembly-0.0.1.jar")

val meta = """META.INF(.)*""".r
assemblyMergeStrategy in assembly := {
    case PathList(ps @ _*) if ps.last == "UnusedStubClass.class" => MergeStrategy.first
	case meta(_) => MergeStrategy.discard
	case x => MergeStrategy.first
}