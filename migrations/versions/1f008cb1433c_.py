"""empty message

Revision ID: 1f008cb1433c
Revises: a5cffa318ac2
Create Date: 2024-02-14 21:16:26.107949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f008cb1433c'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('terrain', sa.Enum('desert', 'grasslands, mountains', 'jungle, rainforests', 'tundra, ice caves, mountain ranges', 'swamp, jungles', name='terrain_types'), nullable=False),
    sa.Column('climate', sa.Enum('arid', 'temperate', 'tropical', 'frozen', 'murky', name='climate_types'), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('orbital_period', sa.Integer(), nullable=False),
    sa.Column('rotation_period', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.Enum('female', 'male', 'other', 'n/a', name='gender_types'), nullable=False),
    sa.Column('birth_year', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('hair_color', sa.Enum('brown', 'blond', 'red', 'black', 'n/a', name='hair_color_types'), nullable=False),
    sa.Column('eye_color', sa.Enum('brown', 'green', 'blue', 'gold', 'n/a', name='eye_color_types'), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('model', sa.String(length=100), nullable=False),
    sa.Column('vehicle_class', sa.Enum('repulsorcraft', 'wheeled', 'starfighter', name='vehicle_class_types'), nullable=False),
    sa.Column('manufacturer', sa.Enum('Incom Corporation', 'Corellia Mining Corporation', name='manufacturer_types'), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('passengers', sa.Integer(), nullable=False),
    sa.Column('pilot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pilot_id'], ['character.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))

    op.drop_table('favorites')
    op.drop_table('vehicle')
    op.drop_table('character')
    op.drop_table('planet')
    # ### end Alembic commands ###