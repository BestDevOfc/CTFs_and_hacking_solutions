<?php

        // The leaked string
        $leakedString = "Sat, 23 Nov 2024 11:27:06 +0000";
        
        // Parse the leaked string into a DateTimeImmutable object
        $leakedDatetime = DateTimeImmutable::createFromFormat("D, d M Y H:i:s O", $leakedString);
        
        if ($leakedDatetime === false) {
            // Handle parsing failure
            echo "Failed to parse the leaked string.\n";
            exit;
        }
        
        // Get the timestamp
        $timestamp = $leakedDatetime->getTimestamp();
        
        // Print the timestamp
        echo "$timestamp";


        
?>