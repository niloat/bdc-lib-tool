<?php

    $file_list = glob("../ck/CK-*");
    $word_list = [];
    foreach($file_list as $file) {
        $db = dbase_open($file, DBASE_RDONLY);

        if(empty($db)) {
            echo "Cannot open db $file\n";
            exit;
        }

        $record_numbers = dbase_numrecords($db);
        echo "$file has $record_numbers records\n";
        for ($i = 1; $i <= $record_numbers; $i++) {
            $row = dbase_get_record_with_names($db, $i);
            /*
            if ($row['ismember'] == 1) {
                echo "Member #$i: " . trim($row['name']) . "\n";
            }
            */
            //print_r($row);
            //echo "current record index: $i\n";

            $record = [];
            foreach($row as $key => $value) {
                $key = iconv('gbk', 'utf-8', $key);
                if($key === false) {
                    $key = '';
                }
                $value = iconv('gbk', 'utf-8', $value);
                if($value === false) {
                    $value = '';
                }
                $record[$key] = $value;
            }
            //print_r($record);
            for($idx=1; $idx<=25; $idx++) {
                $word = trim($record['单词'.$idx]);
                $pronounce = trim($record['音标'.$idx]);
                $mean = trim($record['词意'.$idx]);

                if(strlen($word)==0)
                    continue;
                $word_list[] = array(
                    'w' => $word,
                    'p' => $pronounce,
                    'm' => $mean
                );
            }
        }


        dbase_close($db);
        //print_r($word_list);
    }

    $str = json_encode($word_list, JSON_UNESCAPED_UNICODE);
    file_put_contents("words.json", $str);
    echo "all words: " . count($word_list) . "\n";
