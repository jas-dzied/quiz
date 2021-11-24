extern crate argparse;

use argparse::{ArgumentParser, Store};
use std::fs;
use std::fs::File;
use std::io::prelude::*;

fn main() {

    let mut source = String::new();
    let mut dest = String::from("NULL");

    {
        let mut parser = ArgumentParser::new();
        parser.set_description("Generates a .json file based off a .qz file that follows a simple format");
        parser.refer(&mut source)
              .add_argument("source", Store, "The source file")
              .required();
        parser.refer(&mut dest)
              .add_argument("destination", Store, "The destination file");
        parser.parse_args_or_exit();
    }

    if dest == String::from("NULL") {
        dest = source.clone();
        dest.pop();
        dest.pop();
        dest.push_str("json");
    }

    let contents = fs::read_to_string(source)
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
    let mut file = File::create(dest).expect("Failed to open destination file");
    file.write_all(result.as_bytes()).expect("Failed to write to file");
}
