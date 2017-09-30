<?php

$finder = PhpCsFixer\Finder::create()
    ->in(__DIR__ . '/app')
    ->in(__DIR__ . '/src')
    ->in(__DIR__ . '/tests')
    ->exclude('_generated')
;

return PhpCsFixer\Config::create()
    ->setUsingCache(true)
    ->setRules([
        '@PSR2' => true,
        '@Symfony' => true,
        '@Symfony:risky' => true,
        'strict_param' => true,
        'array_syntax' => ['syntax' => 'short'],
        'linebreak_after_opening_tag' => true,
        'no_multiline_whitespace_before_semicolons' => true,
        'no_php4_constructor' => true,
        'no_short_echo_tag' => true,
        'no_useless_else' => true,
        'ordered_imports' => true,
        'php_unit_construct' => true,
        'phpdoc_order' => true,
        'pow_to_exponentiation' => true,
        'random_api_migration' => true,
        'align_multiline_comment' => true,
        'phpdoc_types_order' => true,
        'no_null_property_initialization' => true,
        'blank_line_before_statement' => true,
        'no_unneeded_final_method' => true,
        'no_unneeded_curly_braces' => true,
        'no_superfluous_elseif' => true,
    ])
    ->setIndent('    ')
    ->setRiskyAllowed(true)
    ->setLineEnding("\n")
    ->setFinder($finder)
    ;
