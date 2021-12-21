#!/usr/bin/perl

# Build config files based on a JSON input file

use strict;
use warnings;

use lib qw(..);

use JSON qw( );

use Template;

# Specify what sort of config to build. This needs to match the template file name
my $conftype   = 'vhost';
my $config_tpl = Template->new();
my $tplfile    = $conftype . '.tt';

my $filename = 'conf.json';

my $cust;
my $custdata;
my $apptag;
my $appdata;
my $custapp;

my $conffile;
my %templatevalues;
my $templatevars;

# Load the JSON file
my $json_text = do {
    open( my $json_fh, "<:encoding(UTF-8)", $filename )
      or die("Can't open \$filename\": $!\n");
    local $/;
    <$json_fh>;
};

# Create the JSON object and decode the loaded file
my $json      = JSON->new;
my $data      = $json->decode($json_text);
my $customers = $data->{'config'};

# Loop over customer and apps and emit a config file for each pairing
while ( ( $cust, $custdata ) = each(%$customers) ) {
    while ( ( $apptag, $appdata ) = each(%$custdata) ) {
        $custapp  = $cust . "-" . $apptag;
        $conffile = $custapp . "-" . $conftype . ".conf";

        # Assemble the values to be passed to the templater
        %templatevalues = (
            custapp  => $custapp,
            cust     => $cust,
            apptag   => $apptag,
            upstream => $appdata->{'upstream'},
            external => $appdata->{'external'}
        );

        $config_tpl->process( $tplfile, { templatedata => \%templatevalues },
            $conffile )
          || die $config_tpl->error();
    }
}
