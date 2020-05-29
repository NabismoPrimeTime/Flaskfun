<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style.css">
	<title>GetCoined | ROI Calculator</title>
	<link rel="icon" href="media/icofile.ico" type="image/x-icon"/>
	<link href="https://fonts.googleapis.com/css2?family=PT+Mono&display=swap" rel="stylesheet">
	<script src="investcalc.js"></script>
</head>
<body>
<div id="global_page">
<div id="global_header">
	<div id="banner_layout">
	<a href="index.html"><img id="banner_img" src="media/banner.png" alt="GetCoined banner"></a>
	<nav id="banner_nav">
	<a id="ROI_Calc" href="index.html">ROI Calculator</a>
	<a href="https://www.getcoined.io/">Home</a>
	</nav>
	</div> <!--banner_layout-->
	</div> <!--global_header-->
	<div id="global_body">
	<div id="mid_body">
	<div id="content_container">
	<div id="blank_space"> 
	</div><!--Blankspace divider-->
	<div id="content">
	<div id="instructions_container">
	<p id="ROI_banner">What is the ROI Calculator?</p>
	<p id="instructions">The GetCoined Return on Investment (ROI) Calculator is a performance measure used to evaluate the 
	efficiency of an investment of bitcoin by calculating the amount of money bitcoin would currently be worth based on your investment
	on a specific date.
	</p>
	</div> <!--instructions_container-->
	<div id="form_container">
	<form action="index.php" method="post"> 
		<div id="date_form">
		<label for="date">Date invested in Bitcoin</label>
		<input id="date_field" name="date" type="date" value="2020-04-01">
		</div> <!--date_form-->
		<div id="invest_form">
		<label for="investment">Amount of investestment</label>
		<span id="currencyinput">$ <input id="invest_field" type="number" name="investment"></span>
		<input type="submit" name="submit" value="Submit" onclick="calcROI();">
		</div> <!--invest_form-->
	</form>
	<?php
	//Check if the form is submitted
	if ( isset ( $_POST['submit'] ) ) {
		//Get Amount of investment from Textfield
		$invest_amt = $_REQUEST['investment'];
		echo '<br>Invest_amt = $' . $invest_amt . '<br>';
		//Get Date invested from Textfield and convert it to alphabetical for use with scraper
		$timestamp = strtotime($_POST['date']); //Get UNIX Timestamp to be parsed to day/month/year
		$day=date('d',$timestamp); //Get Numeric Day
		$month=date('M',$timestamp); //Get Alphabetic Month
		$year=date('Y',$timestamp); //Get Numeric Year
		echo 'month = ' . $month . ' day = ' . $day . ' year = ' . $year . '<br>';
		
		//Link to scraper library
		include('simple_html_dom.php');
		$html =	file_get_html('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130501&end=20200528');
		echo $html->find('td[class="cmc-table__cell cmc-table__cell--sticky cmc-table__cell--left"]',0)->plaintext; //Create table from coinmarketcap.com
	}
	?>
	</div> <!--form_container-->
	</div> <!--content-->
	</div> <!--content_container-->
	</div> <!--mid_body-->
	</div> <!--global_body-->
</div> <!--global_page-->
</body>
</html>
