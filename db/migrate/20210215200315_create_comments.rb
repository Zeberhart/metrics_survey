class CreateComments < ActiveRecord::Migration[5.1]
  def change
    create_table :comments do |t|
      t.string :text
      t.string :source
      t.belongs_to :function

      t.timestamps
    end
  end
end
