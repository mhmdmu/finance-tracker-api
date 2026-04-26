default:
    @just --list

test:
    pytest --no-header --tb=line -ra
