# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20210215200727) do

  create_table "comments", force: :cascade do |t|
    t.string "text"
    t.string "source"
    t.integer "function_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["function_id"], name: "index_comments_on_function_id"
  end

  create_table "comparisons", force: :cascade do |t|
    t.integer "similarity"
    t.integer "comment1_id"
    t.integer "comment2_id"
    t.integer "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["comment1_id"], name: "index_comparisons_on_comment1_id"
    t.index ["comment2_id"], name: "index_comparisons_on_comment2_id"
    t.index ["user_id"], name: "index_comparisons_on_user_id"
  end

  create_table "functions", force: :cascade do |t|
    t.string "fid"
    t.string "name"
    t.string "file"
    t.string "text"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "ratings", force: :cascade do |t|
    t.integer "accurate"
    t.integer "adequate"
    t.integer "concise"
    t.integer "user_id"
    t.integer "comment_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["comment_id"], name: "index_ratings_on_comment_id"
    t.index ["user_id"], name: "index_ratings_on_user_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "email"
    t.string "password_digest"
    t.integer "current_function"
    t.string "current_phase"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
