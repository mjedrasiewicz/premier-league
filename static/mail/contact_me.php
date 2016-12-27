<?php
// Check for empty fields
if(empty($_POST['name'])  		||
   empty($_POST['email']) 		||
   empty($_POST['phone']) 		||
   empty($_POST['message'])	||
   !filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
   {
	echo "No arguments Provided!";
	return false;
   }
	
$name = strip_tags(htmlspecialchars($_POST['name']));
$email_address = strip_tags(htmlspecialchars($_POST['email']));
$phone = strip_tags(htmlspecialchars($_POST['phone']));
$message = strip_tags(htmlspecialchars($_POST['message']));
	
// Create the email and send the message
$to = 'bet.epl.info@gmail.com';
$email_subject = "Website Contact Form:  $name";
$email_body = "Otrzymales nowa wiadomosc z formularza kontaktowego strony.\n\n"."Oto detale:\n\nImie: $name\n\nEmail: $email_address\n\nTelefon: $phone\n\nWiadomosc:\n$message";
$headers = "Od: noreply@gmail.com\n";
$headers .= "Odpowiedz: $email_address";	
mail($to,$email_subject,$email_body,$headers);
return true;			
?>
