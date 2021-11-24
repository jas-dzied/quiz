use std::fs;
use std::fs::File;
use std::io::prelude::*;

const SOURCE_FILE_PATH: &str = "/home/jas/Documents/Programming/Projects/quiz/questions.qz";
const DEST_FILE_PATH: &str = "/home/jas/Documents/Programming/Projects/quiz/questions2.json";

fn main() {
    let contents = fs::read_to_string(SOURCE_FILE_PATH)
        .expect("Failed to open questions source file");

    let quiz_list: Vec<&str> = contents.split("###").collect();
    let mut result = String::new();

    result.push_str("{\n");

    for quiz in quiz_list {
        let questions: Vec<&str> = quiz.split("~~~").collect();
        let quiz_name = String::from(questions[0].trim_matches('\n'));
        result.push_str(&format!("    \"{}\": [\n", quiz_name));
        for question in questions[1..].iter() {
            let parts: Vec<&str> = question.split('\n').collect();
            let parts: Vec<&str> = parts.into_iter().filter(|&i| i != "").collect();

            let question_type = parts[0];
            let question_prompt = parts[1];

            result.push_str(&format!(
                "        {{\n            \"type\": \"{}\",\n            \"prompt\": \"{}\",",
                question_type, question_prompt
            ));

            match question_type {
                "single answer" => {
                    let answer = parts[2];
                    result.push_str(&format!(
                        "\n            \"answer\": \"{}\"\n",
                        answer
                    ));
                },
                "multiple choice" => {
                    let answer = parts[2];
                    let options = &parts[3..];
                    let mut options_builder = String::new();
                    options_builder.push_str(&format!("\n            \"answer\": \"{}\",\n            \"options\": [\n", answer));
                    for option in options.iter() {
                        options_builder.push_str(&format!(
                            "                \"{}\",\n",
                            option
                        ));
                    }
                    options_builder.pop();
                    options_builder.pop();
                    options_builder.push_str("\n            ]\n");
                    result.push_str(&options_builder)
                },
                "options" => {
                    let options = &parts[2..];
                    let mut options_builder = String::new();
                    options_builder.push_str(&format!("\n            \"answers\": [\n"));
                    for option in options.iter() {
                        options_builder.push_str(&format!(
                            "                \"{}\",\n",
                            option
                        ));
                    }
                    options_builder.pop();
                    options_builder.pop();
                    options_builder.push_str("\n            ]\n");
                    result.push_str(&options_builder)
                }
                &_ => panic!("Question type not recognised: {:?}", question_type)
            }
            result.push_str("        },\n");
        }
        result.pop();
        result.pop();
        result.push_str("\n    ],\n");
    }
    result.pop();
    result.pop();
    result.push_str("\n}");
    let mut file = File::create(DEST_FILE_PATH).expect("Failed to open destination file");
    file.write_all(result.as_bytes()).expect("Failed to write to file");
}
